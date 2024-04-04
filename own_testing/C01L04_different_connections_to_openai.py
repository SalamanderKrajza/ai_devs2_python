import sys
sys.path.append(r'..')
import json
from dotenv import load_dotenv
import os
load_dotenv()

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
# openai_apikey = os.environ.get("OPENAI_API_KEY")
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