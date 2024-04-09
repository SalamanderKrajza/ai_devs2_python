import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='people', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
question = task_data['question']

# --------------------------------------------------------------
# Get the data
# --------------------------------------------------------------
import requests

url = "https://tasks.aidevs.pl/data/people.json"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
response = requests.get(url, headers=headers)

content = json.loads(response.text)

# --------------------------------------------------------------
# Convert it into pandas (mostly because i am used to it)
# --------------------------------------------------------------
import pandas as pd
df = pd.DataFrame(content)
df['osoba'] = df['imie'] + " "+ df['nazwisko']
df

# --------------------------------------------------------------
# Get person info
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

chat = ChatOpenAI()
response = chat.invoke(input=
            [
                SystemMessage("pełna forma imienia i nazwisko, nie odpowiadaj na pytanie użytkownika, podaj tylko imię i nazwisko osoby z pytania"),
                HumanMessage(question)
            ]
    )

person_info = df.query(f"osoba=='{response.content}'").to_json()

# --------------------------------------------------------------
# Get answer to question
# --------------------------------------------------------------
response = chat.invoke(input=
            [
                SystemMessage(f"###CONTEXT###\n{person_info}"),
                HumanMessage(question)
            ]
    )

print("Pytanie: ", question)
print("Odpowiedź: ", response.content)

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
data = {"answer": response.content}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)
