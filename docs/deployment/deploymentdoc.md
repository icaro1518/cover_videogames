# Despliegue de modelos

## Infraestructura

- **Nombre del modelo:** cover_videogames
- **Plataforma de despliegue:** CLI a través de Python.
- **Requisitos técnicos:** 
    * Python: 3.9.18
    * Tensorflow: 2.6
    * Numpy: 1.26.0
    * Pandas: 1.5.3
    * mlflow
- **Diagrama de arquitectura:**
![arquitectura](arquitectura.png)

## Código de despliegue

- **Archivo principal:** `src/cover_videogames/mlcli.py`
- **Rutas de acceso a los archivos:** 
    * `hp.db`: archivo con datos de mlflow
    * `src/cover_videogames/mlcli.py` cli para predecir sobre una imagen
    * `mlruns\c90e8a06b2a14ec3ac67910a348fe628` guardado del modelo de MLFlow. 


## Documentación del despliegue

- **Instrucciones de instalación:** (instrucciones detalladas para instalar el modelo en la plataforma de despliegue)
- **Instrucciones de configuración:** (instrucciones detalladas para configurar el modelo en la plataforma de despliegue)
- **Instrucciones de uso:** 
En la terminal, se corre el cli de python, indicando el path al archivo que queremos evaluar.  
```
python src/cover_videogames/mlcli.py --path data\images\u0pi1ltyz2mtmesnxwzq.jpg
```
