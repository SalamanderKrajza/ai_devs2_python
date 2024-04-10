import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='gnome', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
url = task_data['url']

# --------------------------------------------------------------
# Get answer with using OpenAI Vision model
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

human_message = \
    """I will give you a drawing of a gnome with a hat on his head. 
    Tell me what is the color of the hat in POLISH. 
    If any errors occur (f.e image does not have gnome) return "ERROR" as answer
    """

chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=256)
response = chat.invoke([
    HumanMessage(content=[
        {"type": "text", "text": human_message},
        {"type": "image_url", "image_url": {"url": url,"detail": "auto"}}
        ])
    ])
print(response.content)

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
data = {"answer": response.content}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



