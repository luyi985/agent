from .client import model

response = model.invoke("用两句话介绍悉尼。")
print(response)