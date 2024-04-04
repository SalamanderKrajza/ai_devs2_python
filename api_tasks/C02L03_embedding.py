import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='embedding', apikey=apikey)
task_data = get_task_info_from_token(task_token)

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
text_to_get_embeddings = task_data['msg']
just_sentence = text_to_get_embeddings.split(": ")[1]

from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    input=just_sentence,
    model="text-embedding-ada-002"
)
answer = response.data[0].embedding

data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



