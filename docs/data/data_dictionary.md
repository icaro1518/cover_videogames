# Diccionario de datos

## Base de datos 1

| **Variable** | **Descripción** | **Tipo de dato** | **Rango/Valores posibles** |
| --- | --- | --- | --- |
| **FECHA_PRECIO** | Fecha de publicación del precio | String | [1/01/2018, 13/11/2023] |
| **ANIO_PRECIO** | Año de publicación del precio | String | [2018, 2023] |
| **MES_PRECIO** | Mes de publicación del precio | String | [1, 12] |
| **DIA_PRECIO** | Día de publicación del precio | String | [1, 31] |
| **DEPARTAMENTO_EDS** | Departamento de ubicación de la EDS | String | Solo pueden aparecer los 32 departamentos de Colombia |
| **MUNICIPIO_EDS** | Municipio de ubicación de la EDS | String |  |
| **NOMBRE_COMERCIAL_EDS** | Razón Social de la Estación de Servicio | String |  |
| **PRECIO_PROMEDIO_PUBLICADO** | Precio Promedio Mensual por Estación | Númerica | No puede contener valores negativos |
| **TIPO_COMBUSTIBLE** | Tipo de Combustible | String | Solo puede tener el valor GNCV |
| **CODIGO_MUNICIPIO_DANE** | Código Dane del Municipio | String | |
| **LATITUD_MUNICIPIO** | Coordenadas de Georeferenciación del Municipio | String |  |
| **LONGITUD_MUNICIPIO** | Coordenadas de Georeferenciación del Municipio | String |  |

- **Variable**: nombre de la variable.
- **Descripción**: breve descripción de la variable.
- **Tipo de dato**: tipo de dato que contiene la variable.
- **Rango/Valores posibles**: rango o valores que puede tomar la variable.
