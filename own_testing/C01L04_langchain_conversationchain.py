##################################################
# ------------- LangChain conversation
##################################################

# --------------------------------------------------------------
# Created manualy (using list to hold message objects)
# --------------------------------------------------------------

from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = ChatOpenAI()

messages = []

# Save first message
messages.append(HumanMessage("Hello! My Name is Alex"))

#Send it to model and save its response to history
response = chat.invoke(messages)
print(response.content)
messages.append(response)

# Add new message (then we can invoke again)
messages.append(HumanMessage("Tell me my name"))


# --------------------------------------------------------------
# Using ConversationChain implemented in langchain
# --------------------------------------------------------------
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = ChatOpenAI()

conversation = ConversationChain(
    llm=chat, verbose=True, memory=ConversationBufferMemory()
)

response = conversation.predict(input="Hello! My Name is Alex")
print(response)

# Another message. Previous one is already keeped in memory
response = conversation.predict(input="Tell me my name")
print(response)
##################################################
# /------------- /LangChain conversation
##################################################