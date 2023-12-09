# Diccionario de datos

## Base de datos Videojuegos

| **Variable** | **Descripción**                       | **Tipo de dato** | **Rango/valores posibles**                                                                                                                                                     |
|-------------:|---------------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|           id | Id del videojuego en la base de datos | Entero           | Puede ser cualquier dato numérico. En este dataset tenemos datos entre 83 y 279411.                                                                                            |
|        cover |      Id del cover en la base de datos | Entero           | Puede ser cualquier dato numérico. En este dataset tenemos datos entre 10694 y 348557.                                                                                         |
|       genres |                      Lista de géneros | Lista            | Es una lista que puede tener desde 1 elemento hasta 10 en nuestros datos. En esta lista cada elemento es un diccionario que indica el id de ese género y el nombre del género. |
|         name |                 Nombre del videojuego | String           |                                                                                                                                                                                |
|     image_id |       Nombre del archivo de la imagen | String           |                                                                                                                                                                                |

## Base de datos Géneros

| **Variable** | **Descripción**                 | **Tipo de dato** | **Rango/valores posibles**                                                     |
|-------------:|---------------------------------|------------------|--------------------------------------------------------------------------------|
|           id |                   Id del género | Entero           | Puede ser cualquier dato numérico. En este dataset tenemos datos entre 2 y 36. |
|         name |                         Nombre  | String           | Nombre del género                                                              |
|         slug | Nombre del archivo de la imagen | String           | Una versión del nombre única, en minúscula y segura para url                          |