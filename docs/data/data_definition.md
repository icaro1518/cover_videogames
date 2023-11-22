# Definición de los datos

## Origen de los datos

Los datos utilizados provienen de la página de datos abiertos del Gobierno de Colombia (https://www.datos.gov.co/), y son mantenidos y publicados de manera diaria por el Ministerio de Minas y Energía.

Dado que los datos son publicados de manera diaria, se tendrán en cuenta unicamente los registros existentes hasta el día 13 de noviembre de 2023.

## Especificación de los scripts para la carga de datos

Para cargar los datos se hace uso de la API Socrata, una API de datos abiertos que se encuentra implementada en https://www.datos.gov.co/, para hacer uso de ella no es necesario registrarse y el código de carga se encuentra disponible en **scripts/data_acquisition**.

### Rutas de origen de datos

Los datos son almacenados en un único archivo .csv llamado **raw_data** ubicado en una carpeta llamada **data**. Para la transformación y limpieza de los datos, se tienen las siguientes partes:
1. Conversión de fecha_precio a datetime
2. Selección de registros previos al 14 de noviembre de 2023
3. Eliminación de registros con precios nulos
4. Eliminación de datos duplicados
5. Eliminación de columnas con datos redundantes (anio_precio, mes_precio, dia_precio, codigo_municipio_dane)

Al finalizar el preprocesamiento, de igual manera son almacenados en la carpeta **data** bajo el nombre **preprocessed_data** como .csv