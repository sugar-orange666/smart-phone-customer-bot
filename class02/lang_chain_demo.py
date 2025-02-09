from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langfuse.callback import CallbackHandler

import promot_constant
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

handler = CallbackHandler(
    trace_name="多轮对话",
    user_id="songsir",
)

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            promot_constant.messages,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# 多轮对话
def multIChat(userContent):
    # 调用多轮对话链并获取响应
    return chain_with_message_history.invoke(
        {"input": userContent},
        {"configurable": {"session_id": "unused"}, "callbacks": [handler]}).content

    # response = chain_with_message_history.invoke(
    #     {"input": userContent},
    #     {"configurable": {"session_id": "unused"}}
    # ).content

    # 如果响应为空，说明prompt中没有提供信息，需要从数据库中查询
    # if not response:
    #     # 从数据库中查询
    #     db_result = my_db.queryDB(userContent)  # 你需要实现query_db函数
    #     # 将数据库查询结果添加到响应中
    #     response = db_result
    #
    # return response
