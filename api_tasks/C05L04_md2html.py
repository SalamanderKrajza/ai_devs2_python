import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
import json
task_token = get_task_token(taskname='md2html', apikey=apikey)
task_data = get_task_info_from_token(task_token)
print(json.dumps(task_data, indent=4, ensure_ascii=False))
task_data['input']

# --------------------------------------------------------------
# Prepare learning samples - just 5 unique samples, duplicates to make it 10
# --------------------------------------------------------------
data = [
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'**bold**'},{'role':'assistant','content':'<span class="bold">bold</span>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'# header'},{'role':'assistant','content':'<h1>header</h1>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'this is **something** else'},{'role':'assistant','content':'this is <span class="bold">something</span> else'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'## subheader'},{'role':'assistant','content':'<h2>subheader</h2>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'_this_ is **another** else **bold** *example*'},{'role':'assistant','content':'<u>this</u> is <span class="bold">another</span> else <span class="bold">bold</span> <i>example</i>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'**bold**'},{'role':'assistant','content':'<span class="bold">bold</span>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'# header'},{'role':'assistant','content':'<h1>header</h1>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'this is **something** else'},{'role':'assistant','content':'this is <span class="bold">something</span> else'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'## subheader'},{'role':'assistant','content':'<h2>subheader</h2>'}]},
    {'messages':[{'role':'system','content':'I am assistant that converts user input from markdown to html according to USER_XYZ preferences.'},
                 {'role':'user','content':'_this_ is **another** else **bold** *example*'},{'role':'assistant','content':'<u>this</u> is <span class="bold">another</span> else <span class="bold">bold</span> <i>example</i>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'_this_ is else **bold** *example*'},{'role':'assistant','content':'<u>this</u> is else <span class="bold">bold</span> <i>example</i>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'*more* examples *with* just *this* and **bold** for diversion'},{'role':'assistant','content':'<em>more</em> examples <em>with</em> just <u>this</u> and <span class="bold">bold</span> for diversion'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'This has _underscores around_ a **bold** word'},{'role':'assistant','content':'This has <em>underscores around</em> a <span class="bold">bold</span> word'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'*This* is _underline_ and **bold**'},{'role':'assistant','content':'<u>This</u> is <u>underline</u> and <span class="bold">bold</span>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'**Bold**, _lines_, ~~strikethrough~~'},{'role':'assistant','content':'<span class="bold">Bold</span>, <u>lines</u>, <strike>strikethrough</strike>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'Normal **bold _nested_**'},{'role':'assistant','content':'Normal <span class="bold">bold <em>nested</em></span>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'**This _is_ a** ~~test~~'},{'role':'assistant','content':'<span class="bold">This <u>is</u> a</span> <strike>test</strike>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'**Bold _lines_**'},{'role':'assistant','content':'<span class="bold"><u>Bold lines</u></span>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'_Underline_ **bold**'},{'role':'assistant','content':'<u>Underline</u> <span class="bold">bold</span>'}]},
    {'messages':[{'role':'system','content':'I am an assistant that converts user input from markdown to HTML according to USER_XYZ preferences.'},
                 {'role':'user','content':'This **has _nested_**'},{'role':'assistant','content':'This <span class="bold">has <em>nested</em></span>'}]}
]

# NOT WORKING - Expected file to have JSONL format, where every line is a valid JSON dictionary.
# with open("C05L04/training_set.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, ensure_ascii=False)

# Fixed - this time we have list of dictionaries without "," at end of each line
with open("C05L04/training_set.jsonl", "w", encoding="utf-8") as file:
    for single_training_sample in data:
        json.dump(single_training_sample, file, ensure_ascii=False)
        file.write("\n")

# --------------------------------------------------------------
# Upload training dataset to openai - we can see files in https://platform.openai.com/storage
# --------------------------------------------------------------
from openai import OpenAI
client = OpenAI()

uploaded_file = client.files.create(
  file=open("C05L04/training_set.jsonl", "rb"),
  purpose="fine-tune"
)

file_id = uploaded_file.id

# --------------------------------------------------------------
# Train new model with our samples - we can see progress here https://platform.openai.com/finetune
# --------------------------------------------------------------
import time
from datetime import datetime
fine_tuning = client.fine_tuning.jobs.create(
  training_file=file_id, 
  model="gpt-3.5-turbo"
)

fine_tuning_id = fine_tuning.id

# Print events before queue (like validation, creating fine-tuning job etc)
events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=fine_tuning_id, limit=10)
for event in events:
    print(event.message)
print(json.dumps(json.loads(client.fine_tuning.jobs.list_events(fine_tuning_job_id=fine_tuning_id, limit=10).json()), indent=4))

# ----------- MAKE COOFE OR SOMETHING! IT MAY TAKE SOME TIME -----------
# Retrieve the state of a fine-tune from code or here
# https://platform.openai.com/finetune
while True:
    status = client.fine_tuning.jobs.retrieve(fine_tuning_id).status 
    print(f'Status at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} is : {status}')
    time.sleep(60)
    if status not in ['queued', 'running'] :
        break # IT MAY TAKE HOURS TO START! For my 10-samples-dataset i was waiting 30min

# ----------- Another useful endpoints for finetuning -----------
# client.fine_tuning.jobs.cancel(fine_tuning_id) # CANCEL A JOB
# client.models.delete(fine_tuned_model_id) # DELETE A MODEL

# --------------------------------------------------------------
# Use fine-tuned model - assuming that tuning is completed
# --------------------------------------------------------------
model_id = client.fine_tuning.jobs.retrieve(fine_tuning_id).fine_tuned_model

completion = client.chat.completions.create(
  model=model_id,
  messages=[
    {"role": "system", "content": "I am assistant that converts user input from markdown to html according to USER_XYZ preferences."},
    {"role": "user", "content": task_data['input']}
  ]
)
print(completion.choices[0].message.content)

# --------------------------------------------------------------
# Tune fine-tuned model with more samples
# --------------------------------------------------------------
# # more samples:
# more_training_samples = [

# ]

# with open("C05L04/more_training_samples.json", "w", encoding="utf-8") as file:
#     for single_training_sample in more_training_samples:
#         json.dump(single_training_sample, file, ensure_ascii=False)
#         file.write("\n")

# # Upload new file
# uploaded_file2 = client.files.create(
#   file=open("C05L04/training_set.jsonl", "rb"),
#   purpose="fine-tune")
# file_id2 = uploaded_file2.id

# # Initialize new training basing on previous training
# fine_tuning2 = client.fine_tuning.jobs.create(
#   training_file=file_id2, 
#   model=model_id # We are tuning our previously created model
# )
# fine_tuning2.model
# model_id2 = "ft:gpt-3.5-turbo-0125:drtusz::9FUDAoyO"



# --------------------------------------------------------------
# Prepare answer - THIS PART ONLY POINTING OUR API URL
# --------------------------------------------------------------
generated_html = completion.choices[0].message.content
generated_html = generated_html.replace("em>", "u>") # This is fix for api validating _ as underline while most markdowns sees this as <em>
data = {"answer": generated_html}


# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

