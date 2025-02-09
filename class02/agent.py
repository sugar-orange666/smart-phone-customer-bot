# from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool, tool
from datetime import date
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent

import calendar
import dateutil.parser as parser
import my_db

from langchain import hub

#
# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# SERPAPI_API_KEY = "sk-prhpSMx7NYRzx3BMRHp1PDLwqeKRdJFPqapIzJQ36Ilvn5aa"
# _ = load_dotenv(find_dotenv())
# search = SerpAPIWrapper()

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
tools = [
    # Tool.from_function(
    #     func=my_db.test(),
    #     name="Search",
    #     description="useful for when you need to answer questions about current events"
    #
    # ),
    # Tool.from_function(
    #     func=search.run,
    #     name="Search",
    #     description="useful for when you need to answer questions about current events"
    # ),
]


# 自定义工具


@tool("weekday")
def weekday(date_str: str) -> str:
    """Convert date to weekday name"""
    d = parser.parse(date_str)
    return calendar.day_name[d.weekday()]


tools += [weekday]


@tool("content")
def test(content):
    res = agent_executor.invoke(
        {
            "input": content
        }
    )
    print(res)
    return res


tools += [test]


# 下载一个现有的 Prompt 模板
prompt = hub.pull("hwchase17/react")

print(prompt.template)



# 定义一个 agent: 需要大模型、工具集、和 Prompt 模板
agent = create_react_agent(llm, tools, prompt)
# 定义一个执行器：需要 agent 对象 和 工具集
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 执行
agent_executor.invoke({"input": "周杰伦出生那天是星期几"})
