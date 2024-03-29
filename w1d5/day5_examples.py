#############################################################################
# ------------- example 6 - EXTERNAL
#############################################################################

from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
import os
load_dotenv()
import json

system_template = """
# Q: 2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?
# If 2015 is coming in 36 hours, then today is 36 hours before.
today = datetime(2015, 1, 1) - timedelta(hours=36)
# One week from today,
one_week_from_today = today + timedelta(days=7)
# The answer formatted with MM/DD/YYYY is
one_week_from_today.strftime('%m/%d/%Y')

# ... (include other examples as needed, adjusted for Python syntax)

# Q: Jane was born on the last day of February in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?
# If Jane was born on the last day of February in 2001 and today is her 16-year-old birthday, then today is 16 years later.
today = datetime(2001, 2, 28) + timedelta(years=16)
# Yesterday,
yesterday = today - timedelta(days=1)
# The answer formatted with MM/DD/YYYY is
yesterday.strftime('%m/%d/%Y')
"""

human_template = "Q: {question}"

question = "Today is October 13, 2023. What will the date after 193 days from now in the format MM/DD/YYYY?"

formatted_prompt = f"{system_template}\n{human_template.format(question=question)}"

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_template},
        {"role": "user", "content": question}
    ]
)
print(json.dumps(json.loads(response.json()), indent=4))
content = response.choices[0].message.content

import sys
import io
from datetime import datetime
print(content)
if isinstance(content, str):
    exec_date = exec(content, {"print":print})  # Use with caution; ensure safe eval context
    print("Actual Date:", exec_date)

#############################################################################
# ------------- Example 8 - chain of thoughts
#############################################################################
# Import necessary modules
from langchain.prompts import PromptTemplate
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Initialize the chat model
chat = ChatOpenAI(model_name='gpt-4')

# Get the answer using zero-shot prompt
zero_shot_response = chat.invoke([
    SystemMessage('Answer the question ultra-briefly:'),
    HumanMessage('100+48*62-9-100'),
])

print(zero_shot_response.content)

# Get the detailed answer with explanation
chain_of_thought_response = chat.invoke([
    SystemMessage('Take a deep breath and answer the question by carefully explaining your logic step by step. Then add the separator: \n### and answer the question ultra-briefly with a single number:'),
    HumanMessage('100+48*62-9-100'),
])

print(chain_of_thought_response.content)

# Extract the relevant part of the detailed answer
if isinstance(chain_of_thought_response.content, str) and isinstance(zero_shot_response.content, str):
    chain_of_thought_result = chain_of_thought_response.content.split("\n###")[1]
    print(f'Zero Shot: {int(zero_shot_response.content)}', 'Passed' if int(zero_shot_response.content) == 2967 else 'Failed 🙁')
    print(f'Chain of Thought: {int(chain_of_thought_result)}', 'Passed' if int(chain_of_thought_result) == 2967 else 'Failed 🙁')

    