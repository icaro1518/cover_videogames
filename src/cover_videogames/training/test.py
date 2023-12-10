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
from sklearn.preprocessing import MultiLabelBinarizer

dict_modelos = {"efficientnet" : {"model_name" : "EfficientNetB0",
                                  "input_size" : (224, 224, 3),
                                  "decode_predictions" : "efficientnet"},
                "resnet" : {"model_name" : "ResNet50",
                            "input_size" : (224, 224, 3),
                            "decode_predictions" : "resnet"},
                "mobilenet" : {"model_name" : "MobileNet",
                            "input_size" : (224, 224, 3),
                            "decode_predictions" : "resnet"}}

class TestModel():

    def __init__(self, model, model_name, batch_size):
        self.model_name = model_name
        self.batch_size = batch_size
        self.input_size = dict_modelos[model_name]["input_size"]
        self.modelrun = model
        self.test_generator = self.data_generator()
    def data_generator(self):
        all_images = pd.read_csv("data/metadata/games_preprocessed.csv")
        all_images["genres"] = all_images["genres"].apply(lambda x: ast.literal_eval(x))
        train_idx, val_idx = train_test_split(all_images.index, test_size=0.3, random_state=42)
        train_idx, test_idx = train_test_split(train_idx, test_size=0.15, random_state=42)
        test_data = all_images.loc[test_idx]
        return test_data 
    
    def one_hot_multilabel(self, y):
        genres = pd.read_csv("data/metadata/genres_preprocessed.csv")
        genres_dict = genres[["slug", "class_weight"]].set_index("slug").to_dict()["class_weight"]
        id_labels = dict(zip(genres_dict.keys(), list(range(len(genres_dict)))))
        y_id = [[id_labels[lbl_1] for lbl_1 in lbl] for lbl in y]
        # Assuming y_id is your list of lists
        mlb = MultiLabelBinarizer()
        one_hot = mlb.fit_transform(y_id)
        return one_hot
    def load_images(self, df_images):
        # Cargamos el conjunto de datos
        all_images = []
        labels = []
        # Para cada carpeta de cada raza cargamos las imagenes

        for _, row in df_images.iterrows():
            # Cargamos las imágenes con el target size deseado

            all_images.append(np.array(tf.keras.preprocessing.image.load_img(row["image_path"],
                                                                            target_size=self.input_size)))
            labels.append(row["genres"])

        X = np.array(all_images)
        y_one_hot = self.one_hot_multilabel(list(labels))
        return X, y_one_hot
    def test(self):
        test_data = self.data_generator()
        images, y_one_hot = self.load_images(test_data)
        loaded_model = mlflow.pyfunc.load_model(self.modelrun)
        self.predictions = loaded_model.predict(images)
        self.predictions_int = (self.predictions>0.5).astype(int)
        return y_one_hot, self.predictions_int