import sys
sys.path.append(r'..')
import json
from dotenv import load_dotenv
import os
load_dotenv()
openai_apikey = os.environ.get("OPENAI_API_KEY")



messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]

models = ["gpt-4", "gpt-3.5-turbo"]
model = models[1]

##################################################
# ------------- Using models with OpenAI library
##################################################
import openai
# openai.api_key = openai_apikey #Needed if OPENAI_API_KEY has different name

response = openai.chat.completions.create(
            model=model,
            messages=messages)
print(json.dumps(json.loads(response.model_dump_json()), indent=4))

##################################################
# ------------- Using models with requests library
##################################################
import requests
url = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {openai_apikey}"}
data = {"model": model, "messages": messages}
response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=4))


##################################################
# ------------- Streaming example
##################################################
from openai import OpenAI

client = OpenAI() #api_key=openai_apikey

stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")



##################################################
# ------------- Example1 from Course - LangChain INIT
##################################################
# Importowanie odpowiednich klas
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()

# Wywołanie modelu poprzez przesłanie tablicy wiadomości.
# W tym przypadku to proste przywitanie
response = chat.invoke([
    HumanMessage("Hey there!")
])

# Wyświetlenie odpowiedzi
print(response.content)

##################################################
# ------------- Example2 from Course - użycie ChagPromptTemplate
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

# Zwykle do definiowania promptów warto korzystać z template strings
# Tutaj treści zamknięte w klamrach {} są zastępowane przez LangChain konkretnymi wartościami
context = """
The Vercel AI SDK is an open-source library designed to help developers build conversational, streaming, and chat user interfaces in JavaScript and TypeScript. The SDK supports React/Next.js, Svelte/SvelteKit, with support for Nuxt/Vue coming soon.
To install the SDK, enter the following command in your terminal:
npm install ai
"""
system_template = """
As a {role} who answers the questions ultra-concisely using CONTEXT below 
and nothing more and truthfully says "don't know" when the CONTEXT is not enough to give an answer.

context###{context}###
"""
human_template = "{text}"

# Utworzenie promptu z dwóch wiadomości według podanych szablonów:
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template),
])

# Faktyczne uzupełnienie szablonów wartościami
formatted_chat_prompt = chat_prompt.format_messages(
    context=context,
    role="Senior JavaScript Programmer",
    text="What is Vercel AI?",
)

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()
# Wykonanie zapytania do modelu
response = chat.invoke(formatted_chat_prompt)

# Wyświetlenie odpowiedzi
print(response.content)


##################################################
# ------------- Example2 from Course - BEZ ChatPromptTemplate
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

#Generuj wiadomosc sytemu
context = """
The Vercel AI SDK is an open-source library designed to help developers build conversational, streaming, and chat user interfaces in JavaScript and TypeScript. The SDK supports React/Next.js, Svelte/SvelteKit, with support for Nuxt/Vue coming soon.
To install the SDK, enter the following command in your terminal:
npm install ai
"""
role = "Senior JavaScript Programmer"

system_message = f"""
As a {role} who answers the questions ultra-concisely using CONTEXT below 
and nothing more and truthfully says "don't know" when the CONTEXT is not enough to give an answer.

context###{context}###
"""

#Generuj wiadomosc czlowieka
human_message = "What is Vercel AI?"

# odpowiedź
chat = ChatOpenAI()
response = chat.invoke([
    SystemMessage(system_message),
    HumanMessage(human_message),
])

# Wyświetlenie odpowiedzi
print(response.content)

##################################################
# ------------- Example3 from Course - streaming
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage

from langchain_core.callbacks import BaseCallbackHandler
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")

# Inicjalizacja chatu z włączonym streamingiem
chat = ChatOpenAI(streaming=True, callbacks=[MyCustomHandler()])

# Wywołanie chatu wraz z funkcją przyjmującą kolejne tokeny składające się na wypowiedź modelu
chat.invoke([
    HumanMessage(
        "Hey there!"
    ),
])


##################################################
# ------------- Example4 - Tiktoken with library
##################################################
text_to_check = "Cześć, to jest test!"

import tiktoken
encoding = tiktoken.encoding_for_model("gpt-4")
list_of_tokens = encoding.encode(text_to_check)
number_of_tokens = len(list_of_tokens)

print(list_of_tokens, number_of_tokens)


##################################################
# ------------- Example4 - Tiktoken more precise calculations
##################################################
from typing import List, Dict
from tiktoken import get_encoding

def count_tokens(messages: List[Dict[str, str]], model="gpt-3.5-turbo-0613") -> int:
    encoding = get_encoding("cl100k_base")

    tokens_per_message, tokens_per_name = 0, 0

    if model in ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0314", "gpt-4-32k-0314", "gpt-4-0613", "gpt-4-32k-0613"]:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return count_tokens(messages, "gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return count_tokens(messages, "gpt-4-0613")
    else:
        raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3
    return num_tokens

# Przykładowe użycie funkcji count_tokens
messages = [
    {
        "role": "system",
        "content": "Cześć, to jest test!",
    }
]

# Obliczanie liczby tokenów
num = count_tokens(messages, 'gpt-4')
print("Token Count:", num)

# Kodowanie treści wiadomości na tokeny
encoding = tiktoken.encoding_for_model("gpt-4") #get_encoding("cl100k_base")
print("Token IDs:", encoding.encode(messages[0]["content"]))

# PORÓWNANIE Z WYNIKIEM OPENAI
response = openai.chat.completions.create(
            model=model,
            messages=messages)
print("Zuzyte tokeny wg OpenAI: response.usage.prompt_tokens")



##################################################
# ------------- Example5 - Tiktoken more precise calculations
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

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