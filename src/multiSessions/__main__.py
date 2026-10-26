from llmClient import get_model
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
)

model = get_model()

sessions: dict[str, list[BaseMessage]] = {}


def chat(session_id: str, message: str):
    if session_id not in sessions:
        sessions[session_id] = [
            SystemMessage(content="你是旅游助手，用简洁的中文回答。")
        ]

    history = sessions[session_id]
    history.append(HumanMessage(content=message))

    print(f"\n会话 {session_id} 本次发送的历史：")
    for msg in history:
        print(f"{msg.type}: {msg.content}")

    response = model.invoke(history)
    history.append(response)

    print("本次回答：", response.content)
    print("------------")

chat("A", "我计划去悉尼玩三天。")
chat("B", "我计划去墨尔本玩五天。")
chat("A", "我刚才说去哪里，玩几天？")
chat("B", "我刚才说去哪里，玩几天？")