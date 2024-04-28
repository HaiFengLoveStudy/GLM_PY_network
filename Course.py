from zhipuai import ZhipuAI
client = ZhipuAI(api_key="fa80d4c885fde528c1f7bbbc7f6e6f79.HLPSBDLa1Zv4fNv7") # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "你好！你叫什么名字"},
    ],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta)