from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey
    
# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='blogger', apikey=apikey)
task_data = get_task_info_from_token(task_token)

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
outline = task_data['blog']
outline_with_numbers = []
for index, element in enumerate(outline, 1):
    outline_with_numbers.append(f"{index}. {element}")
    
outline_with_numbers

models = ["gpt-4", "gpt-3.5-turbo"]
model = models[1]

import openai
# openai.api_key = openai_apikey #Needed if OPENAI_API_KEY has different name

output=[]
for number in range(1, 5):
    messages = [
        {"role": "system", "content": "Write blog post describing each part of provided outline."},
        {"role": "user", "content": f"Here is the outline {outline}"},
        {"role": "user", "content": f"Generate section for header number {number}"}
        ]
    
    response = openai.chat.completions.create(
            model=model,
            messages=messages)
    output.append(response.choices[0].message.content)
    # print(json.dumps(json.loads(response.model_dump_json()), indent=4))
print(output)

data = {"answer": output}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)
