import sys
sys.path.insert(0, '../..')

import pandas as pd
import numpy as np
np.object = object
np.bool = bool
np.int = int   
np.float = float 
import tensorflow as tf
from sklearn.model_selection import train_test_split
import ast
import mlflow
from cover_videogames.training.data_generator import DataGenerator

dict_modelos = {"efficientnet" : {"model_name" : "EfficientNetB0",
                                  "input_size" : (224, 224, 3),
                                  "decode_predictions" : "efficientnet"},
                "resnet" : {"model_name" : "ResNet50",
                            "input_size" : (224, 224, 3),
                            "decode_predictions" : "resnet"},
                "mobilenet" : {"model_name" : "MobileNet",
                            "input_size" : (224, 224, 3),
                            "decode_predictions" : "resnet"}}
class ModelClassification():
    def __init__(self, model, batch_size, epochs = 30):
        self.model = model
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_name = dict_modelos[model]["model_name"]
        self.input_size = dict_modelos[model]["input_size"]
        self.decode_predictions = dict_modelos[model]["decode_predictions"]
        self.train_generator, self.valid_generator, self.test_generator = self.data_generator()

    @staticmethod
    def new_top(modelo_extractor):
        # Creamos una capa de pooling para consolidar los feature maps de salida en
        # 1024 valores
        pool = tf.keras.layers.GlobalAveragePooling2D()(modelo_extractor.output)
        # Agregamos una capa densa
        dense1 = tf.keras.layers.Dense(units=32, activation="relu")(pool)
        # Agregamos dropout para regularización
        drop1 = tf.keras.layers.Dropout(0.2)(dense1)
        # Agregamos una capa de salida
        dense2 = tf.keras.layers.Dense(units=12, activation="sigmoid")(drop1)
        # Definimos nuestro modelo de transfer learning
        new_model = tf.keras.models.Model(inputs=[modelo_extractor.input], outputs=[dense2])
        return new_model
        
    def generate_model(self):
        modelo_extractor = getattr(tf.keras.applications, self.model_name)(weights='imagenet',
                                                            include_top=False,
                                                            input_shape=self.input_size)
        # Congelamos el extractor de características: transfer_learning
        for layer in modelo_extractor.layers:
            layer.trainable=False
        
        new_model = self.new_top(modelo_extractor)

        return new_model

    def data_generator(self):
        all_images = pd.read_csv("data/metadata/games_preprocessed.csv")
        all_images["genres"] = all_images["genres"].apply(lambda x: ast.literal_eval(x))
        genres = pd.read_csv("data/metadata/genres_preprocessed.csv")
        genres_dict = genres[["slug", "class_weight"]].set_index("slug").to_dict()["class_weight"]
        self.class_weights = dict(enumerate(genres_dict.values()))
        train_idx, val_idx = train_test_split(all_images.index, test_size=0.3, random_state=42)
        train_idx, test_idx = train_test_split(train_idx, test_size=0.15, random_state=42)

        gen = DataGenerator(all_images, genres_dict, train_idx, test_idx, val_idx, seed = 42)
        train_generator, valid_generator, test_generator = gen.all_generators(self.batch_size, self.input_size[:2])
        return train_generator, valid_generator, test_generator
    
    def normal_train(self):
        model = self.generate_model()
        model.compile(loss="categorical_crossentropy",
                optimizer=tf.optimizers.Adam(learning_rate=1e-5),
                metrics=["accuracy"])
        hist_model_efficient, new_model = self.training_model(model, self.train_generator, self.valid_generator,
                                                            save_best_only = False, epochs=self.epochs, 
                                                            batch_size = self.batch_size,
                                                            class_weight = self.class_weights)
                
        score = np.min(hist_model_efficient.history["val_accuracy"])

    @staticmethod
    def training_model(model, train_gen, val_gen,
                   save_best_only = True,
                   path_best_model = "best_model.h5", 
                   epochs = 30, batch_size = 32, class_weight = None):
        if save_best_only:
        # Definimos el callback
            best_callback = tf.keras.callbacks.ModelCheckpoint(filepath=path_best_model,
                                                            monitor="val_loss",
                                                            verbose=True,
                                                            save_best_only=True,
                                                            save_weights_only=True,
                                                            mode="min")
            stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                patience=20,
                                                verbose=0,
                                                mode="auto",
                                                restore_best_weights=True)
            callbacks = [best_callback, stopping]
        else:
            stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                patience=20,
                                                verbose=0,
                                                mode="auto",
                                                restore_best_weights=True)
            callbacks = [stopping]


        # Entrenamos el modelo
        hist_model = model.fit(x=train_gen,
                            validation_data=val_gen,
                            epochs=epochs,
                            steps_per_epoch=train_gen.n//batch_size,
                            callbacks=callbacks
                            )

        return hist_model, model

    def mlflow_run(self, optimizer_name, learning_rate, run_name, exp):
        
        run = mlflow.start_run(run_name=run_name, experiment_id=exp)
        # Generamos nuestro extractor del modelo
        model = self.generate_model()
        
        # Compilamos el modelo con las características a probar del grid search
        metrics = ["accuracy", tf.keras.metrics.AUC(multi_label=True)]

        model.compile(loss="categorical_crossentropy",
                        optimizer=getattr(tf.keras.optimizers, optimizer_name)(learning_rate=learning_rate),
                        metrics=metrics)
        
        hist_model, model = self.training_model(model, self.train_generator, self.valid_generator,
                                                save_best_only = False, epochs=self.epochs, 
                                                batch_size = self.batch_size, class_weight = self.class_weights)
        
        for i in hist_model.epoch:
            metrics = {}
            for metric_name in hist_model.history:
                metrics[metric_name] = hist_model.history[metric_name][i]
            mlflow.log_metrics(metrics, step=i)
        mlflow.log_params({"optimizer" : optimizer_name,
                           "learning_rate" : learning_rate})
        mlflow.tensorflow.log_model(model, "model")        
        mlflow.end_run()
        
        return run, hist_model
    
    def create_gridsearch(self, exp_id):
        optimizadores = ["SGD"]
        learning_rates = [0.00005, 0.00001, 0.000001]
        
        for optimizer in optimizadores:
            for learning_rate in learning_rates:
                run_name = f"{self.model_name}_{optimizer}_{learning_rate}"
                self.mlflow_run(optimizer, learning_rate, run_name, exp_id)


    