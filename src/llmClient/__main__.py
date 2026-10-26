from .client import get_model

model = get_model()
response = model.invoke("用两句话介绍悉尼。")
print(response)