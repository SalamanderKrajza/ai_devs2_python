import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='scraper', apikey=apikey)
task_data = get_task_info_from_token(task_token)
import json
print(json.dumps(task_data, indent=4))
url = task_data['input']
question = task_data['question']

# --------------------------------------------------------------
# SCRAP THE DATA - More advanced version (USING Retry and HTTPAdapter
# --------------------------------------------------------------
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

def request_retry(url, num_retries=10, success_list=[200, 404], kwargs=None):
    if kwargs is None:
        kwargs = {}

    session = requests.Session()
    retry = Retry(
        total=num_retries,
        read=num_retries,
        connect=num_retries,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504], #If any of these then try again
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    attempt = 1
    while attempt <= num_retries:
        try:
            response = session.get(url, headers=headers, **kwargs)
            if response.status_code in success_list:
                print(f"Attempt {attempt} - Success - status {response.status_code}")
                return response
            else:
                status_description = requests.status_codes._codes[response.status_code][0]
                print(f"Attempt {attempt} - Failed - status {response.status_code} - {status_description}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} - Failed - {str(e)}")

        attempt += 1
        return None

    return None

def get_article_text(url):
    response = request_retry(url)
    if response is None:
        return None
    return response.text

article_text = get_article_text(url)

# --------------------------------------------------------------
# SCRAP THE DATA - Without additional imports
# --------------------------------------------------------------
import requests
import time

def request_with_retries(url, max_retries=5, delay=1):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    retries = 0
    while retries < max_retries:
        print(f"Attempt {retries + 1} - ", end="")
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"Success - status {response.status_code}")
                return response
            elif response.status_code in [429, 500, 502, 503, 504]:
                print(f"Failed - status {response.status_code}")
                retries += 1
                time.sleep(delay)
            else:
                print(f" Failed - status {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Failed - {str(e)}")
            retries += 1
            time.sleep(delay)
    
    print(f"Max retries reached. Failed to retrieve the URL.")
    return None

response = request_with_retries(url, max_retries=10, delay=2)
if response is not None:
    article_text = response.text

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
chat = ChatOpenAI(model_name='gpt-3.5-turbo')

system_message = \
f"""Answer user question basing only on knowledge in your context\n
Answer concisely, keep output as short as possible to provide answer\n\n

CONTEXT:\n
{article_text}
"""

response = chat([
    SystemMessage(content=f"Context for user questions is \n\n{system_message}"),
    HumanMessage(content=f"Answer as short as possible\n{question}")
]).content

print(response)

data = {"answer": response}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



