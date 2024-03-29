import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey
from dotenv import load_dotenv
import json
from openai import OpenAI
load_dotenv()   

####################### ZADANIE 1

# Get task info
task_token = get_task_token(taskname='moderation', apikey=apikey)
task_data = get_task_info_from_token(task_token)

task_data

prompts = task_data['input']

# Rozwiązanie
# Test endpointu
client = OpenAI()
response = client.moderations.create(input="Sample text goes here.")
output = response.results[0]
print(json.dumps(json.loads(output.json()), indent=4))
output.flagged

# Rozwiązanie zadania
answer = []
for input in prompts:
    response = client.moderations.create(input=input)
    output = response.results[0]
    if output.flagged:
        answer.append(1)
    else:
        answer.append(0)
print(answer)

#prepare answer
data = {"answer": answer}

#Send answer
response = send_answer_by_task_token(task_token, data)


####################### ZADANIE 2
task_token = get_task_token(taskname='blogger', apikey=apikey)
task_data = get_task_info_from_token(task_token)


outline = task_data['blog']
outline_with_numbers = []
for index, element in enumerate(outline, 1):
    outline_with_numbers.append(f"{index}. {element}")
    
outline_with_numbers

models = ["gpt-4", "gpt-3.5-turbo"]
model = models[1]

import openai
# openai.api_key = openai_apikey #Needed if OPENAI_API_KEY has different name

output=[]
for number in range(1, 5):
    messages = [
        {"role": "system", "content": "Write blog post describing each part of provided outline."},
        {"role": "user", "content": f"Here is the outline {outline}"},
        {"role": "user", "content": f"Generate section for header number {number}"}
        ]
    
    response = openai.chat.completions.create(
            model=model,
            messages=messages)
    output.append(response.choices[0].message.content)
    # print(json.dumps(json.loads(response.model_dump_json()), indent=4))
print(output)

#prepare answer
data = {"answer": output}

#Send answer
response = send_answer_by_task_token(task_token, data)


##################################################
# ------------- LangChain conversation
##################################################
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()


messages = []
messages.append(HumanMessage("Hello! My Name is Alex"))

response = chat.invoke(messages)
messages.append(response)
print(response.content)

messages.append(HumanMessage("Tell me my name"))


# GOTOWIEC:
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Inicjalizacja domyślnego modelu, czyli gpt-3.5-turbo
chat = ChatOpenAI()

# Inicjalizacja konwersacji
# Here it is by default set to "AI"
conversation = ConversationChain(
    llm=chat, verbose=True, memory=ConversationBufferMemory()
)

# Rozpoczęcie konwersacji i wysłanie pierwszej wiadomości
response = conversation.predict(input="Hello! My Name is Alex")
print(response)

# Wysłanie kolejnej wiadomości
response = conversation.predict(input="Tell me my name")
print(response)
##################################################
# /------------- /LangChain conversation
##################################################