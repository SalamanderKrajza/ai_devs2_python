#############################################################################
# ------------- whisper task
#############################################################################
import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='whisper', apikey=apikey)
task_data = get_task_info_from_token(task_token)
url = task_data['msg'].split("file: ")[1]

# --------------------------------------------------------------
# get_file
# --------------------------------------------------------------
import requests
response = requests.get(url)

if response.status_code == 200:
    with open('task_file.mp3', 'wb') as file:
        file.write(response.content)
else:
    print("Access to fille failed")

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
from openai import OpenAI
client = OpenAI()

audio_file= open('task_file.mp3', "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
answer = transcription.text

data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

