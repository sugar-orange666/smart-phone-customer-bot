from langfuse.callback import CallbackHandler
from dotenv import load_dotenv, find_dotenv


from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

_ = load_dotenv(find_dotenv())

handler = CallbackHandler(
    trace_name="SayHello",
    user_id="wzr",
)


model = ChatOpenAI(model="gpt-3.5-turbo-0613")

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("Say hello to {input}!")
])


# 定义输出解析器
parser = StrOutputParser()

chain = (
        {"input": RunnablePassthrough()}
        | prompt
        | model
        | parser
)

res=chain.invoke(input="你是谁", config={"callbacks": [handler]})
print(res)