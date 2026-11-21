"""
Agent 循环：
LLM 请求工具 → 程序执行 → 结果回传 → LLM 继续，直到给出最终回答。
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, TOOL_FUNCTIONS

load_dotenv()  # 从 .env 读取环境变量

API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
MAX_STEPS = 5

if not API_KEY:
    raise SystemExit("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = (
    "你是一个出游推荐助手。用户告诉你城市后，你必须先调用 get_weather 查询明天的天气，"
    "再根据天气推荐一个去处并说明理由（例如下雨推荐室内，晴天推荐户外）。"
    "如果工具返回 error，请如实告诉用户出了什么问题，不要编造天气。"
)

def run_tool(name:str, arguments:str) -> dict:
    """
    执行一次工具调用。
    任何错误都变成 {"error": ...} 交回给 LLM，而不是让程序崩溃。
    """
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return {"error": f"未知工具:{name}"}
    try:
        args = json.loads(arguments)    # LLM 给的参数是 JSON 字符串
        return func(**args)
    except Exception as e:              # 参数格式错、缺参数等
        return {"error": f"工具执行失败:{e}"}

def run_agent(user_input:str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for step in range(1, MAX_STEPS + 1):
        # 对大模型进行请求
        response = client.chat.completions.create(
            model = MODEL,
            messages = messages,
            tools = TOOLS, 
        )
        msg = response.choices[0].message
        print(f"\n===== 第 {step} 轮，发给模型 {len(messages)} 条消息 =====")
        print("模型回复：", msg)


        # 终止条件 1：LLM 不再请求工具，说明它给出了最终回答
        if not msg.tool_calls:
            return msg.content

        # LLM 请求了工具：先把它的“请求”记进对话历史
        messages.append(msg)

        for call in msg.tool_calls:
            print(f"[第 {step} 步] 调用工具 {call.function.name}, 参数 {call.function.arguments}")
            result = run_tool(call.function.name, call.function.arguments)
            print(f"[第 {step} 步] 工具返回 {result}")

            # 把结果以 role=tool 回传，tool_call_id 要对应上
            messages.append({
                "role":"tool",
                "tool_call_id": call.id, 
                "content": json.dumps(result, ensure_ascii=False), 
            })

        # 终止条件 2：超过最大步数
    return f"抱歉，超过最大步数（{MAX_STEPS}）仍未得出结论，已停止。"

