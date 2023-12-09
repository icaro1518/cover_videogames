""" Módulo para realizar el preprocesamiento de los datos
"""
import pandas as pd
import ast
import glob
from pathlib import Path
def preprocesamiento_datos(df: pd.DataFrame) -> pd.DataFrame:
    """ Realiza el preprocesamiento de los datos

    Args:
        df (pd.DataFrame): DataFrame con los datos de los juegos

    Returns:
        pd.DataFrame: DataFrame con los datos preprocesados
    """
    df.drop_duplicates(subset = "name", inplace=True)
    # Cambiar columna de género a lista
    df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x))
    df["genres"]  = df["genres"].apply(lambda list_genres: [d['slug'] for d in list_genres if 'slug' in d])
    df["genres_id"]  = df["genres"].apply(lambda list_genres: [d['id'] for d in list_genres if 'id' in d])
    # Cambio columna image_id para que sea path
    df["image_id"] = df["image_id"]+".jpg"
    # Eliminar columnas innecesarias
    df = df[["genres", "genres_id", "name", "image_id"]]
    return df

# Leer datos
df = pd.read_csv("data/metadata/games.csv")
p = Path('data/images/')

images = list(p.glob('**/*.jpg'))
images_names = [image.name for image in images]
### Preprocesamiento de datos
df = preprocesamiento_datos(df)
df = df[df["image_id"].isin(images_names)]
# Almacenar datos preprocesados
df.to_csv("data/metadata/games_preprocessed.csv", index=False)