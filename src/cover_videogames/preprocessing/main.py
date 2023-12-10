""" Módulo para realizar el preprocesamiento de los datos
"""
import pandas as pd
import ast
import glob
from pathlib import Path
from sklearn.utils.class_weight import compute_class_weight

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
    # Cambio columna image_id para que sea path
    df["image_id"] = df["image_id"]+".jpg"
    # Eliminar columnas innecesarias
    df = df[["genres", "name", "image_id"]]
    return df

# Leer datos
df = pd.read_csv("data/metadata/games.csv")
p = Path('data/images/')

images = list(p.glob('**/*.jpg'))
images_names = [image.name for image in images]
images_df = pd.DataFrame({"image_id": images_names, "image_path": images})
### Preprocesamiento de datos
df = preprocesamiento_datos(df)
df = df.merge(images_df, how = "inner", on = "image_id")

### Filtrando solo los primeros 12 géneros (tener suficiente volumen)
val_counts_genders = df.explode("genres")["genres"].value_counts(normalize=True)
first_12_genres = val_counts_genders.index[:12]
df["genres"] = df["genres"].apply(lambda x: [genre for genre in x if genre in first_12_genres])
df = df[~df["genres"].apply(lambda x:len(x) == 0)]
df.to_csv("data/metadata/games_preprocessed.csv", index=False)

# Crear nuevo dataframe con los géneros filtrados
genres_df = pd.read_csv("data/metadata/genres.csv")
genres_df = genres_df[genres_df["slug"].isin(first_12_genres)]
class_weights = compute_class_weight(class_weight= 'balanced',
                                    classes = first_12_genres.tolist(),
                                    y = df.explode("genres")["genres"])

class_weight_df = pd.DataFrame({"slug": first_12_genres.tolist(), "class_weight": class_weights})
genres_df = genres_df.merge(class_weight_df, how = "inner", on = "slug")

# Almacenar datos preprocesados
genres_df.to_csv("data/metadata/genres_preprocessed.csv", index=False)

