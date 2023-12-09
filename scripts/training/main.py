import mlflow
from scripts.training.model import ModelClassification, dict_modelos

mlflow.set_tracking_uri("http://127.0.0.1:8080/")

for model_name in dict_modelos.keys():
    exp_id = mlflow.create_experiment(name=model_name, artifact_location="mlruns/")
    model = ModelClassification(model_name, 32, 15)
    model.create_gridsearch(exp_id)

