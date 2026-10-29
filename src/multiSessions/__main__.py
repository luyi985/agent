from httpcore import stream

from llmClient import get_model
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    message_chunk_to_message,
    AIMessageChunk
)

model = get_model()

sessions: dict[str, list[BaseMessage]] = {}

def failing_stream():
    yield AIMessageChunk(content="这是")
    yield AIMessageChunk(content="半截回复")
    raise RuntimeError("模拟流中断")


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
    # ------------ Normal Outputs----------------------
    # response = model.invoke(history)
    # history.append(response)

    # print("本次回答：", response.content)
    # ------------ Stream Outputs----------------------
    print("本次回答：", end="", flush=True)
    full_response = None

    for chunk in model.stream(history):
        print(chunk.content, end="", flush=True)
        full_response = (
            chunk if full_response is None
        else full_response + chunk
        )

    if full_response is None:
        raise RuntimeError("流未返回任何消息块")
    
    response = message_chunk_to_message(full_response)
    history.append(response)
    print()
    print("保存的消息类型：", type(response).__name__)
    print("------------")

def failing_chat(session_id: str, message: str):
    if session_id not in sessions:
        sessions[session_id] = [
            SystemMessage(content="你是旅游助手，用简洁的中文回答。")
        ]

    history = sessions[session_id]
    history.append(HumanMessage(content=message))

    print(f"\n会话 {session_id} 本次发送的历史：")
    for msg in history:
        print(f"{msg.type}: {msg.content}")
    full_response = None
    try:
        for chunk in failing_stream():
            print(chunk.content, end="", flush=True)
            full_response = (
                chunk if full_response is None
                else full_response + chunk
            )

        if full_response is None:
            raise RuntimeError("流未返回任何消息块")

        response = message_chunk_to_message(full_response)
        history.append(response)
        print("\n回复完成，已保存。")

    except RuntimeError as exc:
        print(f"\n回复失败，未保存 AI 回复：{exc}")

    print("当前历史角色：", [msg.type for msg in history])
    print("------------")
# chat("A", "我计划去悉尼玩三天。")
# #chat("B", "我计划去墨尔本玩五天。")
# chat("A", "我刚才说去哪里，玩几天？")
# #chat("B", "我刚才说去哪里，玩几天？")


# failing_chat("C", "我计划去巴黎玩四天。")
# failing_chat("C", "我刚才说去哪里，玩几天？")

# def gen_number():
#     c= 0
#     while True:
#         c += 1
#         yield c

# g= gen_number()
# next(g)

# while a := next(g) < 10:
#     print(a)

# failing_chat("C", "我计划去巴黎玩四天。")
# chat("C", "我刚才说去哪里，玩几天？")

# print("最终历史角色：", [msg.type for msg in sessions["C"]])

def my_practice (session_id: str, message: str, stream_fn=model.stream):
    if (session_id not in sessions):
        sessions[session_id] = [
            SystemMessage(content="你是旅游助手，用简洁的中文回答。")
        ]

    history = sessions[session_id]
    print("本次回答：", end="", flush=True)
    print(message)
    history.append(HumanMessage(content=message))

    full_response = None
   
    try:
        for chunk in stream_fn(history):
            print(chunk.content, end="", flush=True)
            full_response = (
                chunk if full_response is None
                else full_response + chunk
            )

        if full_response is None:
            raise RuntimeError("流未返回任何消息块")

        response = message_chunk_to_message(full_response)
        history.append(response)
        print("\n回复完成，已保存。")

    except Exception as exc:
        print(f"\n回复失败，未保存 AI 回复：{exc}")

    print("当前历史角色：", [msg.type for msg in history])
    print("------------")


my_practice("C", "我计划去巴黎玩四天。", stream_fn=failing_stream)
my_practice("C", "我刚才说去哪里，玩几天？")