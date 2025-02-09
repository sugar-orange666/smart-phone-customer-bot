import os
from openai import OpenAI

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

import promot_constant

_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client = OpenAI()
def chatPromot(content):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                # 从文件中加载提示词
                "content": promot_constant.messages

            },
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
    )

    return response.choices[0].message.content


def a(content):
    # 这里只是简单地将输入内容返回作为示例
    return "小木助手: " + chatPromot(content)
