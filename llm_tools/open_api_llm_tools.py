from langfuse.decorators import observe
from langfuse.openai import openai  # OpenAI integration

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


#openapi的格式调用
@observe()
def story():
    return openai.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
            {"role": "system", "content": "你是智能问答助手."},
            {"role": "user", "content": "你是谁"}
        ],
    ).choices[0].message.content


@observe()
def main():
    print(story())
    return story()


main()
