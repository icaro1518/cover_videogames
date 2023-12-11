from argparse import ArgumentParser
import mlflow
import numpy as np
np.object = object
np.bool = bool
np.int = int   
np.float = float 
mlflow.set_tracking_uri("http://127.0.0.1:8080/")
import tensorflow as tf
import pandas as pd
def main():
    parser = ArgumentParser(
            description="CLI para modelo de detección de trabajos fraudulentos"
            )
    parser.add_argument("--path", type=str, required=True, help="path de la imagen a predecir")
    args = parser.parse_args()
    model = mlflow.pyfunc.load_model("models:/cover_videogames/Production")
    image = np.array([tf.keras.preprocessing.image.load_img(args.path,target_size=(224,224,3))])
    prediction = model.predict(image)[0]
    genres = pd.read_csv("data/metadata/genres_preprocessed.csv")
    genres_dict = genres[["slug", "class_weight"]].set_index("slug").to_dict()["class_weight"]
    list_labels = list(genres_dict.keys())
    prediction = [list_labels[i] for i in np.where(prediction > 0.5)[0] if i]
    print(f" {prediction}")

if __name__ == "__main__":
    main()