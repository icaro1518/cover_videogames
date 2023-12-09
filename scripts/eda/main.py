""" Main script for exploratory data analysis (EDA)
"""
import pandas as pd
import numpy as np
np.object = object
np.bool = bool
np.int = int   
np.float = float 

import matplotlib.pyplot as plt
from pathlib import Path
import tensorflow as tf
from collections import Counter
from scripts.preprocessing.main import preprocesamiento_datos
PATH_DATOS = "data/metadata/"
PATH_IMAGENES = "data/images/"

def get_dims(filepath: str) -> tuple:
    """
    Retorna las dimensiones, canales y ubicación
    de una imagen dada
    """
    im = np.array(tf.keras.preprocessing.image.load_img(filepath))
    altura, ancho, canales = im.shape
    return altura, ancho, canales, filepath

df = pd.read_csv(PATH_DATOS + "/games.csv")
df["image_id"] = df["image_id"] + ".jpg"	
p = Path(PATH_IMAGENES)

images_list = list(p.glob('*.jpg'))
images_names = [image.name for image in images_list]
images_df = pd.DataFrame({"image_id": images_names, "image_path": images_list})

# Extensiones archivos 
extensiones_archivos = [path_imagen.suffix for path_imagen in images_list]
print("Extensiones de los archivos")
print(Counter(extensiones_archivos))

# Ejemplo de portadas (9 primeros)
fig = plt.figure(figsize=(10, 10))
rows = 3
columns = 3
contador_posicion = 1

for image_name in images_list[:9]:

    imagen = plt.imread(image_name)
    fig.add_subplot(rows, columns, contador_posicion)
    plt.imshow(imagen)
    plt.axis('off')
    contador_posicion+=1
plt.savefig("docs/data/examples_covers.png")

# Datos faltantes
imagenes = pd.DataFrame(set(images_names), columns=["image_id_img"])
dataset = pd.DataFrame(set(df["image_id"]), columns=["image_id_dataset"])
data_test_2 = imagenes.merge(dataset, how = "outer", left_on = "image_id_img", right_on = "image_id_dataset")
data_test_2["is_in_dataset"] = data_test_2["image_id_dataset"].notnull()
data_test_2["is_in_imagenes"] = data_test_2["image_id_img"].notnull()
print("Relación de imágenes en el dataset y en la carpeta de imágenes")
print(pd.crosstab(data_test_2.is_in_imagenes, data_test_2.is_in_dataset))

# Datos duplicados
print("¿Hay datos duplicados en el dataset?")

print("Id de video juego")
print(len(df.id.unique())== len(df))

print("Cover name file")
print(len(df.image_id.unique())== len(df))

print("Name of the game")
print(len(df.name.unique())== len(df))

# Obtenemos los datos de cada una de nuestras imágenes
tamanios_imagenes = [get_dims(img) for img in images_list]
print(tamanios_imagenes)
df_tamanios_imagenes = pd.DataFrame(tamanios_imagenes,
                                    columns =['Altura', 'Ancho', 'Canales', 'Filepath'])
df_tamanios_imagenes.plot.scatter(x = 'Ancho', y = 'Altura')
plt.title('Tamaño de las imágenes (en pixeles)')
plt.savefig("docs/data/tamanio_imagenes.png")

# Relacion entre variables explicativas y variable objetivo
df_copy =  pd.read_csv(PATH_DATOS + "/games.csv")
df_copy = preprocesamiento_datos(df_copy)

images_df = pd.DataFrame({"image_id": images_names, "image_path": images_list})
df_merged = df_copy.merge(images_df, how = "inner", on = "image_id")
# Imagenes descargadas sin registro en metadatos
fig = plt.figure(figsize=(20, 20))

# Definición valores de cantidad de filas y columnas subplot
rows = 10
columns = 3
contador_posicion = 1

for _, row in df_merged.sample(9, random_state = 1).iterrows():

    imagen = plt.imread(row["image_path"])
    fig.add_subplot(rows, columns, contador_posicion)
    plt.imshow(imagen)
    plt.axis('off')
    plt.title(", ".join((row["genres"][:2])))
    contador_posicion+=1
plt.savefig("docs/data/covers_with_labels.png")