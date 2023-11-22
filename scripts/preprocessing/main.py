import pandas as pd
from matplotlib import pyplot as plt

def preprocesamiento_datos(df):
    # Convertir a datetime fecha_precio
    df["fecha_precio"] = pd.to_datetime(df["fecha_precio"])
    # Obtener registros previos al 14 de noviembre de 2023
    df = df[df["fecha_precio"] <= "2023-11-13"]
    # Eliminar registros con precio nulo
    df = df[df["precio_promedio_publicado"].notnull()]
    # Eliminar registros duplicados
    df = df.drop_duplicates()
    # Remoción variables redundantes
    df = df.drop(columns=["anio_precio", "mes_precio", 
                          "dia_precio", "codigo_municipio_dane"])
    return df

# Leer datos
df = pd.read_csv("data/raw_data.csv")

### Descripción datos

# Revisar existencia de valores nulos
print("Valores nulos: ")
print(df.isnull().sum())

# Revisar existencia de valores duplicados
print("Valores duplicados: ")
print(df.duplicated().sum())

# Revisar existencia de valores atípicos a través de un boxplot 
df.boxplot(column="precio_promedio_publicado")
plt.title("Boxplot precio promedio publicado")
plt.savefig("docs/data/boxplot_precio.png")

# Graficar serie de tiempo (agregada mensual)
df_serie_tiempo = df.copy()
df_serie_tiempo["fecha_precio"] = pd.to_datetime(df_serie_tiempo["fecha_precio"])
df_serie_tiempo = df_serie_tiempo.set_index("fecha_precio")
df_serie_tiempo = df_serie_tiempo["precio_promedio_publicado"].resample("M").mean()
df_serie_tiempo = df_serie_tiempo.reset_index()
df_serie_tiempo.plot(x="fecha_precio", y="precio_promedio_publicado")
plt.title("Serie de tiempo precio promedio (mensual) publicado 2018-2023")
plt.savefig("docs/data/serie_tiempo_precio.png")

### Preprocesamiento de datos

df = preprocesamiento_datos(df)

# Almacenar datos preprocesados
df.to_csv("data_files/preprocessed_data.csv", index=False)