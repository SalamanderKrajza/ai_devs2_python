#############################################################################
# ------------- example 6 - EXTERNAL
#############################################################################
# system_template was recreated (partly) to make it creating python code 

# --------------------------------------------------------------
# IMPORTANT NOTE ABOUT EXEC() AND RECREATING TYPSECRIPT CODE
# --------------------------------------------------------------
# Python is exec() not working exactly as typescript eval()
# Due to fact that i am not using exec often (and i am not sure if i ever need to)
# I found few problems here
# 1. It is not importing liblaries automaticaly. 
# -  I could modify examples to let chat add them, or add them myself
# -  I decided to add them manualy to keep prompts shorter and focus on logic
# 2. It is not returning anything normaly
# -  I could add print() into example but it will not be as useful as variable
# -  I decided to use dictionary that let me access all variables created in exec()


from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
import os
load_dotenv()
import json

system_template =  """
# Q: 2015 is coming in 36 hours. What is the date one week before today in MM/DD/YYYY?
# If 2015 is coming in 36 hours, then today is 36 hours before.
today = datetime(2015, 1, 1) - timedelta(hours=36)
# One week before today,
date_before_1_week = today + timedelta(days=7)
# The answer formatted with MM/DD/YYYY is
date_before_1_week = date_before_1_week.strftime('%m/%d/%Y')

# ... (include other examples as needed, adjusted for Python syntax)

# Q: Jane was born on the last day of February in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?
# If Jane was born on the last day of February in 2001 and today is her 16-year-old birthday, then today is 16 years later.
today = datetime(2001, 2, 28) + timedelta(years=16)
# Yesterday,
yesterday = today - timedelta(days=1)
# The answer formatted with MM/DD/YYYY is
yesterday = yesterday.strftime('%m/%d/%Y')
"""
# --------------------------------------------------------------
# print() VS varname = varname.strftime(...)
# --------------------------------------------------------------
# In case we don't need access to variable later we may replace line
# yesterday = yesterday.strftime('%m/%d/%Y')
# with
# print(yesterday.strftime('%m/%d/%Y'))
# and then we don't need creating outputs dict or knowing "variable name" at the end


human_template = "Q: {question}"

question = "Today is October 13, 2023. What will the date after 193 days from now in the format MM/DD/YYYY?"

formatted_prompt = f"{system_template}\n{human_template.format(question=question)}"

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_template},
        {"role": "user", "content": f"Q: {question}"}
    ]
)
print(json.dumps(json.loads(response.json()), indent=4))
content = response.choices[0].message.content
print(content)

# Add required libs to string
content_with_libs = f"from datetime import datetime, timedelta\n{content}"
content_with_working_newline_character_in_exec = content.replace('\\n', '\n')
if isinstance(content_with_libs, str):
    outputs = {} #Create object that will get all variables created inside exec function
    exec(content_with_libs, outputs) 
    print("Date after 193 days from now is: ", outputs['date_after_193_days'])
