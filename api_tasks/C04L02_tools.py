import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='tools', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
question = task_data['question']

# --------------------------------------------------------------
# Prepare function schema and create model object
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

select_specific_tool_schema = {
    "name": "select_specific_tool",
    "description": "Decide whether the task should be added to the ToDo list or to the Calendar (if time is provided) and return the corresponding JSON.",
    "parameters": {
        "type": "object",
        "properties": {
            "tool": {
                "type": "string",
                "description": "The tool to use, either 'Calendar' or 'ToDo'.",
                "enum": ["ToDo", "Calendar"]
            },
            "desc": {
                "type": "string",
                "description": "The description of the task.",
            },
            "date": {
                "type": "string",
                "description": "The date of the task in YYYY-MM-DD format (only for Calendar tasks)",
            },
        },
        "required": ["tool", "desc"],
    },
}

model_with_functions = ChatOpenAI(
    # model_name="gpt-4-0613",
    model_name="gpt-3.5-turbo",
    model_kwargs={
        "functions": [select_specific_tool_schema],
        "function_call": {"name": "select_specific_tool"}, 
    }
)

# --------------------------------------------------------------
# Prepare context 
# --------------------------------------------------------------
from datetime import date
today = date.today().strftime('%Y-%m-%d')
system_message = f"Current date is {today}"

# --------------------------------------------------------------
# Get the model answer
# --------------------------------------------------------------
result = model_with_functions.invoke([
    SystemMessage(system_message),
    HumanMessage(question)
    ])
function_name = result.additional_kwargs["function_call"]["name"]
function_args = json.loads(result.additional_kwargs["function_call"]["arguments"])

print("Question :", question)
print(json.dumps(function_args, indent=4, ensure_ascii=False))

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
answer = function_args
data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



