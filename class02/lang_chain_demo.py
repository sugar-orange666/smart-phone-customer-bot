from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

import promot_constant

# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
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
    return chain_with_message_history.invoke(
        {"input": userContent}, {"configurable": {"session_id": "unused"}}).content
