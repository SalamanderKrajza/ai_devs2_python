import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='meme', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
image_url = task_data['image']
text = task_data['text']

# --------------------------------------------------------------
# Generate meme
# --------------------------------------------------------------
# This task is in most part about configurating RENDERFORM template
# We need to manualy
# 1. Create template with desired format
# 2. Change background color to black
# 3. Create image object and text object on template
# 4. Update/get image_id and text_id
# 5. Save template
# 6. Update data values to match our template id and text/image ids
import requests
import os
renderform_apikey = os.getenv("RENDERFORM_API_KEY")

url = "https://get.renderform.io/api/v2/render"

# Set the template ID and data for the image
data = {
    "template": "funny-clams-flap-kindly-1950", # Created manualy on renderform
    "data": {
        "text_to_replace.color": "#eeeeee",
        "text_to_replace.text": text,
        "image_to_replace.src": image_url
    }
}

# Set the headers for the API request
headers = {
    "X-API-KEY": renderform_apikey,
    "Content-Type": "application/json"
}

# Send the POST request to the RenderForm API
response = requests.post(url, json=data, headers=headers)

# --------------------------------------------------------------
# prepare answer
# --------------------------------------------------------------
result_url = response.json()['href']
print(result_url)

data={'answer':result_url}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



