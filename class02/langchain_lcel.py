from langchain_core.tools import tool

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import JsonOutputToolsParser
import my_db

from typing import Union
from operator import itemgetter
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableMap,
    RunnablePassthrough,
)


# @tool
# def multiply(first_int: int, second_int: int) -> int:
#     """两个整数相乘"""
#     return first_int * second_int
#
#
# @tool
# def add(first_int: int, second_int: int) -> int:
#     "两个数相加."
#     return first_int + second_int


@tool
def queryDB(content: str) -> str:
    """查询数据库中关于手机的信息，比如价格等"""
    res = my_db.queryDB(content)
    print(res)
    return res


# tools = [multiply, add, queryDB]
tools = [queryDB]
# 带有分支的 LCEL

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# 名称到函数的映射
tool_map = {tool.name: tool for tool in tools}


def call_tool(tool_invocation: dict) -> Union[str, Runnable]:
    """Function for dynamically constructing the end of the chain based on the model-selected tool."""
    tool = tool_map[tool_invocation["type"]]
    return RunnablePassthrough.assign(
        output=itemgetter("args") | tool
    )


call_tool_list = RunnableLambda(call_tool).map()


def route(response):
    if len(response["functions"]) > 0:
        return response["functions"]
    else:
        return response["text"]


llm_with_tools = llm.bind_tools(tools) | {
    "functions": JsonOutputToolsParser() | call_tool_list,
    "text": StrOutputParser()
} | RunnableLambda(route)

# result = llm_with_tools.invoke("共有几种品牌的手机")
# result = llm_with_tools.invoke("你是谁")
# print(result)


def queryDB(content):
    llm_with_tools.invoke(content)
