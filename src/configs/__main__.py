import os
from dotenv import load_dotenv


load_dotenv()

model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("MODEL_BASE_URL")
api_key = os.getenv("MODEL_API_KEY")

# print(model_name)
# print(base_url)
# print(api_key)