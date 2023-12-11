# Despliegue de modelos

## Infraestructura

- **Nombre del modelo:** cover_videogames
- **Plataforma de despliegue:** CLI a través de Python.
- **Requisitos técnicos:** 
    * Python: 3.9.18
    * Tensorflow
    * Numpy
    * Pandas
    * mlflow
```
python -m pip install mlflow, numpy, tensorflow, pandas, protobuf==3.20.*

```
- **Diagrama de arquitectura:**
![arquitectura](arquitectura.png)

## Código de despliegue

- **Archivo principal:** `src/cover_videogames/mlcli.py`
- **Rutas de acceso a los archivos:** 
    * `src/cover_videogames/mlcli.py` cli para predecir sobre una imagen
    * `mlruns\c90e8a06b2a14ec3ac67910a348fe628` guardado del modelo de MLFlow. 
    * `mlruns\models\`: Carpeta que especifica el modelo productivo

## Documentación del despliegue

- **Instrucciones de instalación:**
Se instalan las librerías a través de la siguiente configuración con la versión 3.9 de Python.
```
conda create -n myenv3 python=3.9
conda activate myenv3
python -m pip install mlflow, numpy, tensorflow, pandas, protobuf==3.20.*

```

- **Instrucciones de configuración:** 
Activar servidor de mlflow
```
mlflow server --host 127.0.0.1 -p 8080
```
Luego de activado el servidor, se puede usar el cli sin problema como aparece en el siguiente punto.

- **Instrucciones de uso:** 
En la terminal, se corre el cli de python, indicando el path al archivo que queremos evaluar.  
```
python src/cover_videogames/mlcli.py --path data\images\u0pi1ltyz2mtmesnxwzq.jpg
```
