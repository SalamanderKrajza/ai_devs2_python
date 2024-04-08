import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey
from dotenv import load_dotenv
import json
from openai import OpenAI
load_dotenv()   

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='moderation', apikey=apikey)
task_data = get_task_info_from_token(task_token)

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
prompts = task_data['input']

# Test endpoint
client = OpenAI()
response = client.moderations.create(input="Sample text goes here.")
output = response.results[0]
print(json.dumps(json.loads(output.json()), indent=4))
output.flagged

# Complete task
answer = []
for input in prompts:
    response = client.moderations.create(input=input)
    output = response.results[0]
    if output.flagged:
        answer.append(1)
    else:
        answer.append(0)
print(answer)

data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

