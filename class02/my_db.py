from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_community.agent_toolkits import create_sql_agent

_ = load_dotenv(find_dotenv())
from langchain_community.utilities import SQLDatabase

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
# 连接到本地 MySQL 数据库
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:1566729swj@localhost:3306/product")

# chain = create_sql_query_chain(llm, db)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)


def queryDB(content):
    res = agent_executor.invoke(
        {
            "input": content
        }
    )
    print(res)
    return res
