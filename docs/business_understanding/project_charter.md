# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Clasificación del género de videojuegos a través de sus portadas

## Objetivo del Proyecto

El objetivo es crear una herramienta que pueda predecir cuáles son los posibles géneros que lo identifiquen. 
## Alcance del Proyecto

Se tomarán los datos de las portadas de videojuegos de Xbox Series S|X, Nintendo Switch y Play Station 5 y con esto se generá un clasificador. 

### Datos
Los datos disponibles son 7303 imágenes registros de Xbox Series S|X, Nintendo Switch y Play Station 5. Estos son tomados a través de una API operada por Twitch llamada IGDB. Mayor información sobre este conjunto de datos se puede encontrar en [Link](https://api-docs.igdb.com/?python#authentication)

### Resultados esperados

Se espera obtener un modelo de predicción de los géneros, el modelo no indicará cuál es el género si no cuáles podrían ser todos los géneros que podrían asignarle a cierta portada. 

## Metodología

Se seguirá la metodología CRISP-DM para la exploración y modelamiento del problema, donde se tiene como variable los géneros asociados a un juego y se hará la predicción a través de las portadas de los juegos. Para esto se utilizarán varios modelos de redes neuronales con un modelo Multi Label para así poder asignar todos los géneros asociados a una portada. 

## Cronograma

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos | 1 1/2 semanas | del 7 al 17 de noviembre |
| Preprocesamiento, análisis exploratorio | 1/2 semana | del 18 al 21 de noviembre |
| Modelamiento y extracción de características | 1 semana | del 22 al 28 de noviembre |
| Despliegue | 1 semana | del 29 de noviembre al 5 de diciembre |
| Evaluación y entrega final | 1/2 semanas | del 6 de diciembre al 9 de diciembre |

## Equipo del Proyecto

- Desarrollado por **Heiler Santiago Gómez Prieto**
