#############################################################################
# ------------- FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################
# The process is described in api_tasks/C04L04/C04L04_README.md
# The API that is preparing answer is in api_tasks/C04L04/C04L04_FLASKAPI.py
# The course task_functions to point api adress are in api_tasks/C04L04_ownapi.py
#############################################################################
# /------------- /FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################

import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='ownapi', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))

# --------------------------------------------------------------
# Prepare answer - THIS PART ONLY POINTING OUR API URL
# --------------------------------------------------------------
data = {"answer": "https://c7d3-109-231-63-108.ngrok-free.app/"}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



