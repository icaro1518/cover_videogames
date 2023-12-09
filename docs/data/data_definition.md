# Definición de los datos

## Origen de los datos

Los datos tienen como origen la página IGDB.com. Esta página tiene como propósito ser la página definitiva para videojuegos, donde se puede encontrar toda la información de videojuegos desde las portadas, divididas por generación, plataforma, año hasta por ejemplo el rating de los videojuegos. Para poder consultar la información de esto se puede realizar a través de una API (https://api-docs.igdb.com/#getting-started). 

## Especificación de los scripts para la carga de datos


Para cargar los datos se hace uso de IGDB, se cargan los datos a través de la API encontrada en la siguiente documentación https://api-docs.igdb.com/#getting-started, para hacer uso de ella hay que seguir una serie de pasos y obtener un token de la página de developers de Twitch. El código se encuentra en `scripts/data_acquisition` y en se hace la llamada a la API para poder diferentes características de los videojuegos y las portadas de los mismos.

### Rutas de origen de datos

Los datos estarán almacenados en la carpeta `/data`, y como datos finales vamos a tener 3 csv's y 7303 imágenes. 
1. `/data/metadata/genres.csv` csv con los géneros que tiene la api. Indica un id para cada uno de los géneros. 
2. `/data/metadata/games.csv` csv con todos los videojuegos. Para cada uno de estos se tendrá los géneros asociados y más información.
3. `/data/metadata/games_preprocessed.csv` csv con todos los videojuegos con la informaición ya preprocesada. 

Adicionalmente, las 7303 imágenes estarán asociadas con cada uno de los videojuegos se encontrarán en la carpeta de `/data/images`. 

