import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='rodo', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4))

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
answer = \
r"""Hello! I need you to tell me about yourself, however we have some privacy problems here.
You CANNOT send me any personal information about you. We need to cover them with some placeholders!

List of placeholders to include (you should include all of them):
%imie%, %nazwisko%, %zawod% and %miasto%"

Make sure you separate %imie% and %nazwisko%
"""
data = {"answer": answer}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



