# Get task data
import os
from dotenv import load_dotenv
load_dotenv()

apikey = os.environ.get("APIKEY")
import requests

# Get task token
def get_task_token(taskname, apikey):
    url = f'https://tasks.aidevs.pl/token/{taskname}'
    data = {"apikey": apikey}
    response = requests.post(url, json=data)
    print("Status: ", response.status_code)

    if response.status_code == 200:
        print("Odpowiedź: \n")
        print(response.json())
        return response.json()['token']
    else:
        print(f"Błąd: Nie udało się uzyskać tokenu.")
        return False
    
# Get your task data from task_token
def get_task_info_from_token(task_token):
    url = f'https://tasks.aidevs.pl/task/{task_token}'
    response = requests.post(url)
    print("Status: ", response.status_code)

    if response.status_code == 200:
        print("Odpowiedź: \n")
        print(response.json())
        return response.json()
    else:
        print(f"Błąd: Nie udało się uzyskać tokenu.")
        return False
    
# Send answer
def send_answer_by_task_token(task_token, data):
    url = f'https://tasks.aidevs.pl/answer/{task_token}'

    response = requests.post(url, json=data)
    print(response.status_code)
    print(response.json())
    return response.json()