from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey
    
# Get task info
task_token = get_task_token(taskname='helloapi', apikey=apikey)
task_data = get_task_info_from_token(task_token)

#prepare answer
cookie = task_data['cookie']
data = {"answer": cookie}

#Send answer
response = send_answer_by_task_token(task_token, data)



