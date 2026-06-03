import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_API_BASE"),
)
# 同步调用
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {"role": "system", "content": "你是一个诗人。"},
        {"role": "user", "content": "用诗描述一下你。"}
    ],
)
print("【同步输出】", response.choices[0].message.content)
print("\n" + "=" * 50 + "\n")

# 流式调用
print("【流式输出】", end="")
stream = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {"role": "user", "content": "用 3 个要点介绍 Transformer 架构。"}
    ],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()