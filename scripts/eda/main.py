""" Main script for exploratory data analysis (EDA)
"""
import pandas as pd
import glob
import matplotlib.pyplot as plt
from pathlib import Path
PATH_DATOS = "datos/metadata/"
PATH_IMAGENES = PATH_DATOS + "images/images/"

def get_dir_size(path: str) -> float:
    """
    Obtiene el tamaño en MB de un directorio dado
    """
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total / 1024 ** 2

def get_dims(filepath: str) -> tuple:
    """
    Retorna las dimensiones, canales y ubicación
    de una imagen dada
    """
    im = np.array(tf.keras.preprocessing.image.load_img(filepath))
    altura, ancho, canales = im.shape
    return altura, ancho, canales, filepath


def load_images(path_datos: str, target_size: tuple):
    # Cargamos el conjunto de datos
    all_images = []
    labels = []
    # Para cada carpeta de cada raza cargamos las imagenes
    temp_path = path_datos + "/"
    for im_path in os.listdir(temp_path):
        # Cargamos las imágenes con el target size deseado

        all_images.append(np.array(tf.keras.preprocessing.image.load_img(temp_path+im_path,
                                                                        target_size=target_size)))

    X = np.array(all_images)
    y = np.array(labels)

    return X, y
df = pd.read_csv("data/metadata/games.csv")
p = Path('data/images/')

images = list(p.glob('data/images/*.jpg'))
images_names = [image.name for image in images]

imagenes = pd.DataFrame(set(images_names), columns=["image_id_img"])
dataset = pd.DataFrame(set(df["image_id"]), columns=["image_id_dataset"])
data_test_2 = imagenes.merge(dataset, how = "outer", left_on = "image_id_img", right_on = "image_id_dataset")
data_test_2["is_in_dataset"] = data_test_2["image_id_dataset"].notnull()
data_test_2["is_in_imagenes"] = data_test_2["image_id_img"].notnull()
print(pd.crosstab(data_test_2.is_in_imagenes, data_test_2.is_in_dataset))

imagenes_total = glob.glob(PATH_IMAGENES+"*")
imagenes_total[:5]