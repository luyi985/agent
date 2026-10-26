from .client import get_model
from langchain_core.prompts import ChatPromptTemplate


# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是旅游助手，用简洁的中文回答。"),
#     ("human", "用两句话介绍{city}，重点说明它是否适合{travel_style}。"),
# ])
# #formatted_prompt = prompt.invoke(city="悉尼", travel_style="休闲") 
# formatted_prompt = prompt.invoke({
#     "city": "悉尼",
#     "travel_style": "休闲",
# })

# model = get_model()
# response = model.invoke(formatted_prompt)
# print(formatted_prompt.to_messages())
# print('----------------')
# print(response.content)
# print('----------------')
# print(response.response_metadata)

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

model = get_model()

# 会话开始时，只添加一次
messages = [
    SystemMessage(content="你是旅游助手，用简洁的中文回答。")
]

# 第一轮
messages.append(HumanMessage(content="介绍一下悉尼。"))
response = model.invoke(messages)
print(response.content)
print('----------------')
messages.append(response)

# 第二轮
messages.append(HumanMessage(content="那里适合亲子游吗？"))
response = model.invoke(messages)
messages.append(response)

print(response.content)
