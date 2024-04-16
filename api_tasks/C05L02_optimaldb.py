import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='optimaldb', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
database = task_data['database']


# --------------------------------------------------------------
# Get data
# --------------------------------------------------------------
import requests

url = database = task_data['database']

response = requests.get(url)
json_data = response.json()

with open("C05L02/orginal_data.json", "w", encoding="utf-8") as file:
    json.dump(json_data, file, indent=4, ensure_ascii=False)

# --------------------------------------------------------------
# Optimize with LLMLingua to compress database [DONT WORK WITH TASK, works in playground]
# --------------------------------------------------------------
# LLMLingua is a library to optimize prompts by removing "not-important" words while keeping it meaningful to LLM
# I just wanted to test how it will handle database optimization
# More information available here: https://github.com/microsoft/LLMLingua
from llmlingua import PromptCompressor
llm_lingua = PromptCompressor(
    model_name="microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
    use_llmlingua2=True, # Whether to use llmlingua-2
    device_map="cpu"  # Use CPU instead of GPU
)
compressed_prompt = llm_lingua.compress_prompt(str(json_data), rate=0.33, force_tokens = ['\n', '?'])
comppressed_prompt_text = compressed_prompt['compressed_prompt']

# Due to fact that compressed prompts lost JSON structure i've adding HEADERS by simply replacing first occurance of name in data
# Normally i would probably split data to compress user-by-user
comppressed_prompt_text = comppressed_prompt_text.replace("zygfryd", "### List of facts about Zygfryd\nZygfryd")
comppressed_prompt_text = comppressed_prompt_text.replace("Stefan", "\n\n### List of facts about Stefan\nStefan", 1)
comppressed_prompt_text = comppressed_prompt_text.replace("Ania", "\n\n### List of facts about Ania\nAnia",1)
print(comppressed_prompt_text)

with open("C05L02/compressed_prompt.txt", "w", encoding="utf-8") as file:
    file.write(comppressed_prompt_text)

# --------------------------------------------------------------
# Optimize json by LLM [DONT WORK WITH TASK, works in playground]
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
chat = ChatOpenAI(model="gpt-4")
system_message = \
"""You are an AI assistant tasked with optimizing a JSON database. The database contains information about people and facts associated with them. 
Your goal is to reduce the size of the database while preserving all the essential information.

I will provide part of data for specific user (only one). All facts are related to that user.
Your role is to convert these facts into as brief and conside version as possible. Skip all unnessesery words. Remove person name (it will be listed above).
We want to have each of them brief but keep all important informations about person.
You don't need to keep enire sentences (we can just juse keywords).
Make sure you don't skip any fact from list. You want to keep all of them in your final output.

Example:
Orginal: Dumnie Zygfryd przedstawia swoje umiejętności w sztukach walki, którym oddaje się regularnie, ćwicząc aikido.
Simplified: Zygfryd ćwiczy aikido


Original JSON:
"""

optimized_data = {}
for name, facts in json_data.items():
    response = chat.invoke(input=
                [
                    SystemMessage(system_message),
                    HumanMessage(str(json_data[name]))
                ]
        )
    print("Odpowiedź dla: ", name, "\n", response.content)
    optimized_data[name] = response.content
print(optimized_data)


with open("C05L02/optimized_data.json", "w", encoding="utf-8") as file:
    json.dump(optimized_data, file, indent=4, ensure_ascii=False)

# --------------------------------------------------------------
# Summarization instead of conversion [Works with task]
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
chat = ChatOpenAI(model="gpt-4")
system_message = \
"""You are an AI assistant tasked with optimizing a JSON database. The database contains information about people and facts associated with them. 
Your goal is to reduce the size of the database while preserving all the essential information.

I will provide part of data for specific user (only one). All facts are related to that user.
Your role is to convert these facts into as brief and conside summary. Skip all unnessesery words.
You don't need to keep enire sentences (we can just juse keywords).
Make sure you don't skip any fact from list. You want to keep all of them in your final output.

Your summary should be plain text (don't need to keep it as list, don't need to use quotes)
Keep responses in Polish language
"""

summarized_data = {}
for name, facts in json_data.items():
    response = chat.invoke(input=
                [
                    SystemMessage(system_message),
                    HumanMessage(str(json_data[name]))
                ]
        )
    print("Odpowiedź dla: ", name, "\n", response.content)
    summarized_data[name] = response.content
print(summarized_data)


with open("C05L02/summarized_data.json", "w", encoding="utf-8") as file:
    json.dump(summarized_data, file, indent=4, ensure_ascii=False)

# --------------------------------------------------------------
# prepare answer
# --------------------------------------------------------------

data={'answer':comppressed_prompt_text} # Works in playground, do not pass the task
data={'answer':str(optimized_data)} # Works in playground, do not pass the task
data={'answer':str(summarized_data)} # Works with task


# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



