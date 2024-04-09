import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='knowledge', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
question = task_data['question']

# --------------------------------------------------------------
# Select the knowledge soruce
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

select_source_schema = {
    "name": "select_source",
    "description": "Select knowledge source from specified list basing on question content",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Unchanged user question"
            },
            "knowledge_source": {
                "type": "string",
                "description": "currency (if user ask exhange rates) population (if user asks about population of the country), other (otherwise)",
                "enum": ["currency", "population", "general"]
            },
            "currency": {
                "type": "string",
                "description": "3-digits Code for specific currency, f.e USD, PLN, EUR",
            },
            "country": {
                "type": "string",
                "description": "Name of country from question in English, f.e Poland, Germany, United Kingdo",
            },
            "answer": {
                "type": "string",
                "description": "Answer for user question. Required if knowledge_source is 'general'",
            },
        },
        "required": [
            "knowledge_source", "question", "answer"
        ]
    }
}

model_with_functions = ChatOpenAI(
    # model_name="gpt-4-0613",
    model_name="gpt-3.5-turbo",
    model_kwargs={
        "functions": [select_source_schema],
        "function_call": {"name": "select_source"}, 
    }
)

result = model_with_functions.invoke([HumanMessage(question)])
function_name = result.additional_kwargs["function_call"]["name"]
function_args = json.loads(result.additional_kwargs["function_call"]["arguments"])

print("Question :", question)
print(json.dumps(function_args, indent=4, ensure_ascii=False))
# --------------------------------------------------------------
# Get the answer
# --------------------------------------------------------------
import requests
def get_currency_rate(currency_code="USD"):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_code}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    rate = json.loads(response.content)['rates'][0]['mid']
    return rate

def get_country_population(country_name="POLAND"):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    population = json.loads(response.content)[0]['population']
    return population

if function_args["knowledge_source"] == "currency" and "currency" in function_args: 
    currency_code = function_args['currency']
    answer = get_currency_rate(currency_code)

elif function_args['knowledge_source'] == "population" and "country" in function_args:
    country_name = function_args['country']
    answer = get_country_population(country_name)

elif function_args['knowledge_source'] == "general" and "answer" in function_args:
    answer = function_args['answer'] # answer should be generated while source was selected

else:
    print("Something wentt wrong.")
    print("Model should choose knowledge_sources and generate related fields")
    print("Question :", question)
    print(json.dumps(function_args, indent=4, ensure_ascii=False))

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
print(answer)
data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



