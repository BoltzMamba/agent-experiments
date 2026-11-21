"""
工具层：
真正干活的函数 + 给 LLM 看的工具说明书。
"""

# 模拟的"明天天气"。故意不接真实天气 API，把注意力放在 Agent 循环上。
FAKE_WEATHER = {
    "北京": {"condition": "晴", "temp_low": 3, "temp_high": 12},
    "上海": {"condition": "小雨", "temp_low": 10, "temp_high": 15},
    "广州": {"condition": "多云", "temp_low": 18, "temp_high": 25},
    "成都": {"condition": "阴", "temp_low": 9, "temp_high": 14},
}

def get_weather(city: str) -> dict:
    """
    返回明天的模拟天气。
    城市不存在时返回 error，而不是抛异常。
    """
    city = city.strip().removesuffix("市")
    if city in FAKE_WEATHER:
        return {"city":city, **FAKE_WEATHER[city]}
    return {
        "error":f"没有找到城市「{city}」的天气数据", 
        "supported_cities": list(FAKE_WEATHER.keys()),
    }

# 给 LLM 看的"说明书"（OpenAI function calling 格式）。
# LLM 看不到上面的 Python 代码，只能看到这里的 name / description / parameters。
TOOLS = [       # ① 列表：可以放多个工具
    {
        "type": "function",     # ② 工具类型
        "function": {           # ③ 这个函数的具体说明
            "name": "get_weather", 
            "description": "查询某个城市明天的天气（天气状况和最低/最高气温，单位摄氏度）。", 
            "parameters": {     # ④ 参数说明
                "type": "object",       # 参数整体是一个对象（字典）
                "properties":{          # 这个对象里有哪些字段
                    "city": {"type":"string", "description": "城市中文名，例如：北京"}
                },
                "required":["city"],    # 哪些字段必须提供
            },
        },
    }
]

# 工具名 → 真实函数，agent.py 用它按名字找函数
TOOL_FUNCTIONS = {"get_weather": get_weather}