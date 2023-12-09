import pandas as pd
import numpy as np
np.object = object
np.bool = bool
np.int = int   
np.float = float 
import tensorflow as tf
from sklearn.model_selection import train_test_split
import ast
from scripts.training.data_generator import DataGenerator

all_images = pd.read_csv("data/metadata/games_preprocessed.csv")
all_images["genres"] = all_images["genres"].apply(lambda x: ast.literal_eval(x))
genres = pd.read_csv("data/metadata/genres_preprocessed.csv")
genres_dict = genres[["slug", "id"]].set_index("slug").to_dict()["id"]
train_idx, test_idx = train_test_split(all_images.index, test_size=0.3, random_state=42)
train_idx, val_idx = train_test_split(train_idx, test_size=0.15, random_state=42)

gen = DataGenerator(all_images, genres_dict, train_idx, test_idx, val_idx, seed = 42)
train_generator, valid_generator, test_generator = gen.all_generators(32, (224, 224))