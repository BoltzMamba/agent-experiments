from openai import APIError, AuthenticationError

from agent import run_agent

def main():
    # 获得城市信息
    city = input("你明天想去哪个城市玩？").strip()
    if not city:
        print("没有输入城市。")
        return
    try:
        # 根据城市信息获得天气，和游玩场所推荐
        answer = run_agent(f"我明天想去{city}，推荐我去那里玩？")
        print("\n助手：", answer)
    # 错误信息处理
    except AuthenticationError:
        print("API key 无效，请检查 .env。")
    except APIError as e:
        print(f"调用模型 API 出错：{e}")

if __name__ == "__main__":
    main()