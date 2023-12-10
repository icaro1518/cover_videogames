import sys
sys.path.insert(0, 'C://Users//mface//cover_videogames//src')

from cover_videogames.training.test import TestModel
from sklearn.metrics import classification_report

test = TestModel(model = "runs:/712454f6885349f1ba4f4a2d2233d399/model",
                 model_name="efficientnet",
                 batch_size=32,)

y_one_hot, predictions_int = test.test()
print("===========================================================")
print("==============Clasification Report - EfficientNet==========")
print("\n")
print(classification_report(y_one_hot, predictions_int))
print("\n")
print("===========================================================")


test = TestModel(model = "runs:/c90e8a06b2a14ec3ac67910a348fe628/model",
                 model_name="resnet",
                 batch_size=32,)

y_one_hot, predictions_int = test.test()
print("===========================================================")
print("==============Clasification Report - ResNet==========")
print("\n")
print(classification_report(y_one_hot, predictions_int))
print("\n")
print("===========================================================")


test = TestModel(model = "runs:/aac44e0148a442fd9dc6ce9b878011f0/model",
                 model_name="mobilenet",
                 batch_size=32,)

y_one_hot, predictions_int = test.test()
print("===========================================================")
print("==============Clasification Report - MobileNet==========")
print("\n")
print(classification_report(y_one_hot, predictions_int))
print("\n")
print("===========================================================")
