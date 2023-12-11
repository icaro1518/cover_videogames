# Informe de salida

## Resumen Ejecutivo

El modelo para predecir los géneros de un videojuego es un proyecto haciendo uso de una variable de salida multilabel, en donde podremos predecir más de una categoría para cada videojuego. Se probaron múltiples modelos y no tuvieron los mejores resultados. Se puede a futuro mejorar y probar nuevas cosas con el modelo para poder tener una solución más robusta. 

## Resultados del proyecto

- Para este proyecto se entrenaron 3 Modelos variando sus hiperparámetros de Optimizadores y learning Rate. Teniendo como "mejor" modelo el ResNet. 
- El modelo tiene muchas oportunidades de mejora agregando más datos y entrenando a través de un fine tuning o una red custom.
- El modelo en generar el da una probabilidad muy alta a todas las categorías y no es muy funcional. Hay que iterar sobre este para poder generar un modelo más robusto. 

## Lecciones aprendidas

- La obtención de los datos a partir del API puede llegar a ser muy complicado, entendiendo los limitantes de la herramienta.
- No tenía conocimientos de los modelos multilabel entonces fue interesante abordarlo.
- Hubo varios conflictos con Optuna y MLFlow con el modelo de Tensorflow, generaba un error entonces se optó por hacer un gridsearch con las oportunidades.
- No se pudo fácilmente desplegar un modelo de CNN a través de MLFlow, ya que este modelo deseaba directamente los datos a predecir y con la imagen se necesitaba es el path en particular para poder tener la predicción.

## Impacto del proyecto

- El modelo puede tener mejores resultados a través de sus métricas, es posible reducir el número de categorías o aumentar los datos para no tener tantos problemas de desbalance.

## Conclusiones

- Se logró implementar de inicio a fin el desarrollo de un modelo siguiendo la metodología de CRISP-DM.
- Se puede entrenar un mejor modelo buscando un fine tuning y ajustando un poco mejor los datos y outputs.

