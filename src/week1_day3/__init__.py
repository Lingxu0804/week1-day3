
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors


def main() -> None:
    # 1. 加载 API Key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("未找到 GEMINI_API_KEY")
        return

    # 2. 创建模型客户端
    client = genai.Client(api_key=api_key)

    # 3. 创建聊天会话
    chat = client.chats.create(
        model="gemini-3.5-flash-lite"
    )

    print("===== 我的第一个 AI 聊天助手 =====")
    print("输入 exit 可以退出对话")

    # 4. 开始循环对话
    while True:
        question = input("\n你：").strip()

        if question.lower() in ("exit", "quit", "退出"):
            print("对话结束")
            break

        if not question:
            continue

        try:
            response = chat.send_message(question)

            print(f"\nGemini：{response.text}")

            # 5. 统计每轮 Token 使用量
            usage = response.usage_metadata

            if usage:
                print(
                    f"\n本轮输入 Token："
                    f"{usage.prompt_token_count}"
                )
                print(
                    f"本轮输出 Token："
                    f"{usage.candidates_token_count}"
                )

        except errors.APIError as error:
            print(f"API 请求失败：{error.code}")
            print(error.message)


    # 查看本次会话历史
    history = chat.get_history()

    print("\n===== 本次会话历史 =====")
    print(f"历史消息数：{len(history)}")

    for message in history:
        print(f"消息角色：{message.role}")        

if __name__ == "__main__":
    main()
