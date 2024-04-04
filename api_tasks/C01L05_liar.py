import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
# NOTE - this is different than previous because this time /get_task_info requires additional context
task_token = get_task_token(taskname='liar', apikey=apikey)

import requests
url = f'https://tasks.aidevs.pl/task/{task_token}'
data = {
    "question": "Odpowiedz jednym słowem używając małych liter: Jaki kolor ma trawa?"
}
response = requests.post(url, data=data)
print(response.status_code, response.json())

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
response.json()['answer']

if response.json()['answer'] == "zielony":
    answer = 'YES'
else:
    answer = 'NO'

data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



