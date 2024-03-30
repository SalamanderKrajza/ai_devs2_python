import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey
from dotenv import load_dotenv
load_dotenv()   

######## ZADANIE

# Get task info
task_token = get_task_token(taskname='inprompt', apikey=apikey)
task_data = get_task_info_from_token(task_token)

question = task_data['question']
print(question)

import pandas as pd
df = pd.DataFrame({'inputs':task_data['input']})


from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
model = ChatOpenAI()
name_to_filter_dataset = model([
    SystemMessage(content="""
        User will provide some question in polish.
        Respond with name of person described in probided question.
        Return only the name and nothing else.
    """),
    HumanMessage(content=f"Question: {question}")
]).content
print(name_to_filter_dataset)


filtered_df = df.query(f'inputs.str.contains("{name_to_filter_dataset}")')
filtered_df.inputs.to_list()

answer = model([
    SystemMessage(content=f"""
        User will provide some question in polish.
        You should respond to his question also in polish.
                  
        To provide answer use context below (and only context).
        
        ### context:
        {filtered_df.inputs.to_list()}
    """),
    HumanMessage(content=f"Question: {question}")
]).content
print(answer)


#prepare answer
data = {"answer": answer}

#Send answer
response = send_answer_by_task_token(task_token, data)

