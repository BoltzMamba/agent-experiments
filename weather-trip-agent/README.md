# 天气出游小助手（weather-trip-agent）

一个最小的工具调用 Agent：LLM 先调用天气工具查询明天的天气，再根据天气推荐去哪里玩。用来体会"调用工具 → 读取结果 → 继续执行"的基本循环。

- 模型：DeepSeek API，通过 OpenAI Python SDK 调用
- 工具：`get_weather(city)`，返回模拟的明天天气
- 不使用 Agent 框架

## 文件结构

| 文件 | 职责 |
|---|---|
| `tools.py` | 工具函数 `get_weather`、模拟天气数据，以及给 LLM 看的工具说明 `TOOLS` |
| `agent.py` | Agent 循环：调用 LLM、执行工具、回传结果、判断终止 |
| `main.py` | 入口：读取用户输入，打印最终回答，处理 API 错误 |
| `requirements.txt` | 依赖：`openai`、`python-dotenv` |

## 运行

需要 Python 3.10 及以上版本。以下命令都在仓库根目录 `agent-experiments` 下的 PowerShell 中执行。

1. 创建并激活虚拟环境，安装依赖：

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r weather-trip-agent\requirements.txt
   ```

   如果 `Activate.ps1` 提示禁止运行脚本，先执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，再重新激活。

2. 配置 API key：把根目录的 `.env.example` 复制为 `.env`，然后把 `DEEPSEEK_API_KEY` 改成自己的 key。

   ```powershell
   Copy-Item .env.example .env
   ```

   key 可以在 DeepSeek 开放平台创建。`DEEPSEEK_MODEL` 默认是 `deepseek-chat`。

3. 运行：

   ```powershell
   python weather-trip-agent\main.py
   ```

   输入城市名后，终端会打印每一轮发给模型的消息条数、模型的回复，以及工具的调用参数和返回结果，最后打印助手的推荐。

## 支持的城市

天气是模拟数据，只支持以下城市：

| 城市 | 明天天气 | 气温 |
|---|---|---|
| 北京 | 晴 | 3～12℃ |
| 上海 | 小雨 | 10～15℃ |
| 广州 | 多云 | 18～25℃ |
| 成都 | 阴 | 9～14℃ |

输入其他城市时，工具会返回错误信息和支持的城市列表，Agent 会把问题告诉用户，而不是直接崩溃。

## 终止条件

- 模型不再请求调用工具，说明它已经给出最终回答。
- 循环超过最大步数（`agent.py` 中的 `MAX_STEPS = 5`）。

## API key 安全

- key 只放在根目录的 `.env` 里。`.env` 已写入 `.gitignore`，不会被提交。
- 代码通过 `python-dotenv` 读取 `.env`，不在任何 `.py` 文件中写死 key。
- 如果 key 泄露，到 DeepSeek 控制台删除它并重新创建。

## 相关笔记

- [Agent 学习记录 01：什么是 Agent](https://boltzmamba.github.io/learning-garden/notes/agent-learning-01/)：本实验对应的概念笔记
