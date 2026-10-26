from configs import model_name, base_url, api_key
from langchain.chat_models  import init_chat_model

def validate_model_params():
    if not model_name:
        raise ValueError("MODEL_NAME is not set.")
    if not base_url:
        raise ValueError("BASE_URL is not set.")
    if not api_key:
        raise ValueError("API_KEY is not set.")

def get_model():
    validate_model_params()
    model = init_chat_model(
        model=model_name,
        model_provider="openai",
        base_url=base_url,
        api_key=api_key,
        use_responses_api=False,
    )
    return model