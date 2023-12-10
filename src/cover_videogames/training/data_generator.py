import tensorflow as tf
import numpy as np
class DataGenerator():
    def __init__(self, all_images, genres_dict, train_idx, test_idx, val_idx, seed = 42):
        self.all_images = all_images
        self.classes=genres_dict.keys()
        self.train_idx = train_idx
        self.test_idx = test_idx
        self.val_idx = val_idx
        self.seed = seed
        self.image_generators()
    
    def image_generators(self):
        self.datagen=tf.keras.preprocessing.image.ImageDataGenerator(width_shift_range=0.3,
                                                            height_shift_range=0.3,
                                                            shear_range=0.2,
                                                            horizontal_flip=True,
                                                            fill_mode='constant')
        self.test_datagen=tf.keras.preprocessing.image.ImageDataGenerator()


    def all_generators(self, batch_size, target_size):
        train_generator=self.datagen.flow_from_dataframe(
            dataframe=self.all_images.loc[self.train_idx],
            directory="./data/images",
            x_col="image_id",
            y_col="genres",
            batch_size=batch_size,
            seed=self.seed,
            shuffle=True,
            classes = self.classes,
            class_mode="categorical",
            target_size=target_size,
            save_to_dir = "data/augmented_images/train/",
            save_format = "jpg")

        valid_generator=self.test_datagen.flow_from_dataframe(
            dataframe=self.all_images.loc[self.val_idx],
            directory="./data/images",
            x_col="image_id",
            y_col="genres",
            batch_size=batch_size,
            seed=self.seed,
            shuffle=True,
            classes = self.classes,
            target_size=target_size,
            class_mode="categorical")

        test_generator=self.test_datagen.flow_from_dataframe(
            dataframe=self.all_images.loc[self.test_idx],
            directory="./data/images",
            x_col="image_id",
            batch_size=1,
            seed=self.seed,
            shuffle=False,
            classes = self.classes,
            target_size=target_size,
            class_mode=None)
        return train_generator, valid_generator, test_generator