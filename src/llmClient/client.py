from configs import model_name, base_url, api_key
from langchain.chat_models  import init_chat_model



model = init_chat_model(
    model=model_name,
    model_provider="openai",
    base_url=base_url,
    api_key=api_key,
    use_responses_api=False,
)
