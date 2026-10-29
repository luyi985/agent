from llmClient import get_model
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

def get_attraction(location: str):
    
    data = {
        "悉尼": "悉尼歌剧院、邦迪海滩",
        "墨尔本": "联邦广场、皇家植物园",
    }
    return data.get(location, "没有该城市的景点资料")


def get_attraction_activities(location: str):
    data = {
        "悉尼歌剧院": "悉尼歌剧院观看演出，欣赏高雅艺术",
        "联邦广场": "购物，参观展览，品尝美食",
        "皇家植物园": "参观植物园，欣赏花卉，散步",
        "邦迪海滩": "海滩冲浪，阳光沙滩，海鲜美食"
    }
    return data.get(location, "没有该城市的景点活动资料")



tool_mapping= {
    "get_attraction_tool": get_attraction,
    "get_attraction_activities_tool": get_attraction_activities
}


@tool
def get_attraction_tool(location: str):
    """查询指定城市的景点，城市名使用中文。"""
    return get_attraction(location)


@tool
def get_attraction_activities_tool(location: str):
    """查询指定景点的活动，景点名使用中文。"""
    return get_attraction_activities(location)

model = get_model()
model_with_tools = model.bind_tools([get_attraction_tool, get_attraction_activities_tool])


def planning( request: str):
    prompt = f"""
    你是一个旅游规划助手
    根据用户的需求：{request}
    请为用户规划该城市的旅游行程，包括景点和活动。

    返回 一个json字符串，包含景点和活动信息。
    示例：
    {{
        "景点": ["悉尼歌剧院", "邦迪海滩"],
        "活动": ["观看演出，欣赏高雅艺术", "海滩冲浪，阳光沙滩，海鲜美食"]
    }}
    """
    plan = model.invoke([SystemMessage(content=prompt)])
    # print(prompt)
    print(plan.content)
    return plan.content


def verify_plan(result: str, plan:str):
    response = model.invoke([
        SystemMessage(
            content="你是行程审核助手，只返回包含 is_valid 和 reason 的 JSON 对象。"
        ),
        HumanMessage(
            content=f"用户需求：{result}\n待审核行程：{plan}"
        ),
    ])
    print("验证正文：", repr(response.content))
    return response.content
   

   






def travel_agent(request: str):
    messages = [
        SystemMessage(content="你是旅游助手，查询景点时使用工具。"),
        HumanMessage(content="我想去悉尼看表演"),
    ]

    max_attempts = 1
    attempt = 0
    result= ""
    while attempt < max_attempts:
        response = model_with_tools.invoke(messages)
        # print("回复内容：", response.content)
        # print("工具调用：", response.tool_calls)
        if not response.tool_calls:
            print("没有调用工具")
        else:
            print("调用了工具")
            first_tool_call = response.tool_calls[0]
            name= first_tool_call.get("name")
            arguments = first_tool_call["args"]
            print("第一次调用的工具信息：", first_tool_call)
            print("调用的工具参数：", arguments)
            print("调用的工具名称：",name)
            if name in tool_mapping:
                tool_result = tool_mapping[name](**arguments)
                print("工具调用结果：", tool_result)
                messages.append(HumanMessage(content=f"工具调用结果：{tool_result}"))


        verification_result = verify_plan(request, "\n".join([m.content for m in messages]))
        if '"is_valid": true' in verification_result:
            return response.content
        attempt += 1
    return "无法生成有效的行程"


# planning("我想去悉尼看表演")
# print("response", response)
travel_agent("我想去悉尼看表演")
