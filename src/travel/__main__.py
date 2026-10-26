from llmClient import get_model
from langchain_core.prompts import ChatPromptTemplate

from .model import TravelRequest

model = get_model()
# request = TravelRequest(
#     city="悉尼",
#     days=3,
#     children=2,
#     interests=["海滩"],
# )

# print(request)

##------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "只提取用户明确提供的旅行信息，不推荐、不推测。"
     "未提供的天数返回 null，兴趣仅保留用户明确表达的内容。"),
    ("human", "{message}"),
])


# prompt.append(("human", "{message}"))
structured_model = model.with_structured_output(TravelRequest)
## --------------------
def structured_model_separately(message: str):
    prompt_value = prompt.invoke({"message": message})
    print("提示词类型：", type(prompt_value))

    output = structured_model.invoke(prompt_value)
    print("结果类型：", type(output))
    return output

##----------------------

# request = structured_model.invoke(
#     prompt.invoke({
#         "message": "我最近心情不好"
#     })
# )
structured_output = prompt| structured_model

# output = structured_output.invoke({
#     "message": "我最近心情不好，想去悉尼找女朋友玩两天"
# })

# print(type(output))
# print(output)
##-------------------------------

def validate_days(output)-> list[str]:
    issues= []
    if output.days is None:
        issues.append("追问：你准备玩几天？")
    elif output.days <= 0:
        issues.append("提示：旅行天数必须大于零，请重新提供。")
    return issues


messages = [
    "我想去悉尼玩，带两个孩子",
    "我想去悉尼玩三天，带两个孩子，喜欢海滩。",
    "我想去悉尼玩，带两个孩子，喜欢海滩。",
    "我想去悉尼玩零天，带两个孩子，喜欢海滩。",
    "我想去悉尼玩几天，带两个孩子，喜欢海滩。",
    ""
]
# for message in messages:
#     # output = structured_output.invoke({
#     #     "message": message
#     # })
#     #print("输入：", message)
#     output = structured_model_separately(message)
#     issues = validate_days(output)

#     if issues:
#         for issue in issues:
#             print(issue)
#     else:
#         print("没有发现问题。")
#         print("结果：", output.model_dump())
#     print('------------')

# --------Batch process-----------------------
# inputs = [prompt.invoke({"message": message}) for message in messages]
# inputs = [{"message": message} for message in messages]
inputs= [{}, {"message": "我想去悉尼玩三天，带两个孩子，喜欢海滩。"},]
outputs = structured_output.batch(inputs, config={"max_concurrency":3},return_exceptions=True,)

for input_data, output in zip(inputs, outputs):
    print("输入：", input_data)

    if isinstance(output, Exception):
        print("调用或解析失败：", output)
    else:
        print("提取结果：", output.model_dump())
        issues = validate_days(output)

        if issues:
            for issue in issues:
                print(issue)
        else:
            print("没有发现问题。")

    print("------------")