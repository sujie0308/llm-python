"""
CLI 交互式客户端 - 在终端中和 AI 对话
功能：
- 输入文字和 AI 对话（流式输出）
- clear 清空对话历史
- show 查看历史消息
- quit 退出程序
"""

# 从 llm_client.py 中导入 LLMClient 类
from llm_client import LLMClient


def main():
    """主函数：创建客户端并进入交互循环"""
    # 创建 LLM 客户端（自动读取 .env 配置）
    client = LLMClient()
    print("LLM CLI 启动（quit退出 / clear清空历史 / show查看历史）\n")

    # 无限循环：一直等待用户输入，直到用户说 quit
    while True:
        # 等待用户输入，strip() 去除首尾空格
        user_input = input("你: ").strip()

        # 如果输入为空，跳过本次循环
        if not user_input:
            continue

        # 退出命令
        if user_input == "quit":
            break

        # 清空对话历史
        if user_input == "clear":
            client.reset()
            print("历史已清空\n")
            continue

        # 查看对话历史
        if user_input == "show":
            client.show_history()
            continue

        # 正常对话：用流式方式调用 AI
        print("AI: ", end="", flush=True)  # flush=True 立即输出，不缓存
        for chunk in client.stream_chat(user_input):
            print(chunk, end="", flush=True)  # 逐字打印（打字机效果）
        print("\n")


# 当直接运行本文件时执行 main()
# 如果被别的文件 import，不会自动执行
if __name__ == "__main__":
    main()