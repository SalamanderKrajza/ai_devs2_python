##################################################
# ------------- Example5 - Tiktoken more precise calculations
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
import json

# Wersja nie dzialajaca (__call__ bierze cala historie)

chat = ChatOpenAI()
memory = ConversationBufferWindowMemory(k=1)
chain = ConversationChain(llm=chat, memory=memory)

response1 = chain.__call__("Hey there! I'm Adam")
print("AI:", response1)

response2 = chain.__call__("Hold on.")
print("AI:", response2)

# Tutaj model "zapomina" imię, ponieważ "k" jest ustawione na 1. Wcześniejsza wiadomość została ucięta.
response3 = chain.__call__("Do you know my name?")
print("AI:", response3)


print(json.dumps(json.loads(chain.json()), indent=4))

# Wersja dzialajaca (predict uwzglednia parametr k)

chat = ChatOpenAI()
memory2 = ConversationBufferWindowMemory(k=1)
chain2 = ConversationChain(llm=chat, memory=memory2)

response1 = chain2.predict(input="Hey there! I'm Adam")
print("AI:", response1)

response2 = chain2.predict(input="Hold on.")
print("AI:", response2)

# Tutaj model "zapomina" imię, ponieważ "k" jest ustawione na 1. Wcześniejsza wiadomość została ucięta.
response3 = chain2.predict(input="Do you know my name?")
print("AI:", response3)

print(json.dumps(json.loads(chain2.json()), indent=4))
