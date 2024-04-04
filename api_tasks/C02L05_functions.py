import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='functions', apikey=apikey)
task_data = get_task_info_from_token(task_token)
import json
print(json.dumps(task_data, indent=4))

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
answer = {
            "name": "addUser",
            "description": "add user to database",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "provide name of user"
                    },
                    "surname": {
                        "type": "string",
                        "description": "provide surname of user"
                    },
                    "year": {
                        "type": "integer",
                        "description": "provide users year of born"
                    },
                }
            }
        }

data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



