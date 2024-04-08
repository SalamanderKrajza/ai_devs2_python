import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

#############################################################################
# ------------- MANUAL CREATING A CONVERSATION
#############################################################################
# --------------------------------------------------------------
# Get task token (more data will be acquiret while asking for hints)
# --------------------------------------------------------------
task_token = get_task_token(taskname='whoami', apikey=apikey)
print("\n\n")

# --------------------------------------------------------------
# prepare answer
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
chat = ChatOpenAI(model_name='gpt-3.5-turbo')

system_message = \
f"""### INSTRUCTION:
Your role is to guess the person basing on hints provided by user
You must ask for hints as long, as you would be absolutly certian about the answer

### RULES:
- You have only 2 possibilities
- Ask for next hint by writing "NEXT"
- Provide answer by writinng the correct name

### Example:
User: Hint1: He was born long ago
AI: NEXT
User: Hint2: He has only one leg
AI: NEXT
"""

messages = [
    SystemMessage(content=system_message),
]

for hint_number in range(1,11):
    # --------------------------------------------------------------
    # Add next hint to the conversation
    # --------------------------------------------------------------
    task_data = get_task_info_from_token(task_token, enable_printing=False)
    if 'hint' in task_data:
        hint = task_data['hint']
    else:
        print("#"*50,"\nToken is not active anyomore")
        break

    human_message = f"Hint{hint_number}: {hint}"
    print("Human:", human_message)
    messages.append(HumanMessage(content=human_message))

    # --------------------------------------------------------------
    # Get model answer
    # --------------------------------------------------------------
    response = chat.invoke(messages)
    print("AI: ", response.content)
    messages.append(response)
    if response.content != "NEXT":
        print("#"*50,"\nWE HAVE THE RESPONSE!\n", response.content)
        break
        
data = {"answer": response.content}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

#############################################################################
# ------------- Using langchain ConversationChain with passing systemprompt as user message
#############################################################################
# --------------------------------------------------------------
# Get task token (more data will be acquired while asking for hints)
# --------------------------------------------------------------
task_token = get_task_token(taskname='whoami', apikey=apikey)
print("\n\n")

# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

chat = ChatOpenAI(model_name='gpt-3.5-turbo')

system_message = """
### INSTRUCTION:
Your role is to guess the person based on hints provided by the user.
You must ask for hints as long as you are not absolutely certain about the answer.

### RULES:
- You have only 2 possibilities:
- Ask for the next hint by writing "NEXT"
- Provide the answer by writing the correct name

### Example:
User: Hint1: He was born long ago
AI: NEXT
User: Hint2: He has only one leg
AI: NEXT

### Start of conversation:
"""

memory = ConversationBufferMemory(memory_key="history")

conversation = ConversationChain(
    llm=chat, 
    memory=memory,
    # verbose=True # Prints all messages while predicting response
)

# Pass the system message as the first user message
response = conversation.predict(input=system_message)
print("AI:", response)


for hint_number in range(1, 11):
    # --------------------------------------------------------------
    # Add next hint to the conversation
    # --------------------------------------------------------------
    task_data = get_task_info_from_token(task_token, enable_printing=False)
    if 'hint' in task_data:
        hint = task_data['hint']
    else:
        print("#"*50,"\nToken is not active anyomore")
        break

    human_message = f"Hint{hint_number}: {hint}"
    print("Human:", human_message)

    # --------------------------------------------------------------
    # Get model answer (it's automatically saved to memory)
    # --------------------------------------------------------------
    response = conversation.predict(input=human_message)
    print("AI:", response)

    if response != "NEXT":
        print("#" * 50)
        print(f"AFTER {hint_number} HINTS WE HAVE THE RESPONSE !\n", response)
        break

data = {"answer": response}

# --------------------------------------------------------------
# Send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

#############################################################################
# ------------- Using langchain ConversationChain with passing TEMPLATE into prompt arg
#############################################################################
# --------------------------------------------------------------
# Get task token (more data will be acquiret while asking for hints)
# --------------------------------------------------------------
task_token = get_task_token(taskname='whoami', apikey=apikey)
print("\n\n")

# --------------------------------------------------------------
# prepare answer
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

chat = ChatOpenAI(model_name='gpt-3.5-turbo')

template = """
### INSTRUCTION:
Your role is to guess the person based on hints provided by the user.
You must ask for hints as long as you are not absolutely certain about the answer.

### RULES:
- You have only 2 possibilities:
- Ask for the next hint by writing "NEXT"
- Provide the answer by writing the correct name

### Example:
User: Hint1: He was born long ago
AI: NEXT
User: Hint2: He has only one leg
AI: NEXT

{chat_history}
Human: {input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "input"], 
    template=template
)

memory = ConversationBufferMemory(memory_key="chat_history")

conversation = ConversationChain(
    llm=chat, 
    memory=memory,
    prompt=prompt,
    # verbose=True # Prints all messages while predicting response
)

for hint_number in range(1, 11):
    # --------------------------------------------------------------
    # Add next hint to the conversation
    # --------------------------------------------------------------
    task_data = get_task_info_from_token(task_token, enable_printing=False)
    if 'hint' in task_data:
        hint = task_data['hint']
    else:
        print("#"*50,"\nToken is not active anyomore")
        break

    human_message = f"Hint{hint_number}: {hint}"
    print("Human:", human_message)

    # --------------------------------------------------------------
    # Get model answer (it's automaticaly saved to memory)
    # --------------------------------------------------------------
    response = conversation.predict(input=human_message)
    print("AI: ", response)

    if response != "NEXT":
        print("#" * 50)
        print(f"AFTER {hint_number} HINTS WE HAVE THE RESPONSE !\n", response)
        break

data = {"answer": response}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)

#############################################################################
# ------------- Using langchain ConversationChain with updating .template property
#############################################################################
# --------------------------------------------------------------
# Get task token (more data will be acquiret while asking for hints)
# --------------------------------------------------------------
task_token = get_task_token(taskname='whoami', apikey=apikey)
print("\n\n")

# --------------------------------------------------------------
# prepare answer
# --------------------------------------------------------------
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

chat = ChatOpenAI(model_name='gpt-3.5-turbo')
memory = ConversationBufferMemory(memory_key="history")

conversation = ConversationChain(llm=chat, memory=memory)
conversation.prompt.template = \
"""System: ### INSTRUCTION:
Your role is to guess the person based on hints provided by the user.
You must ask for hints as long as you are not absolutely certain about the answer.

### RULES:
- You have only 2 possibilities:
- Ask for the next hint by writing "NEXT"
- Provide the answer by writing the correct name

### Example:
User: Hint1: He was born long ago
AI: NEXT
User: Hint2: He has only one leg
AI: NEXT
{history}
Human: {input}
Assistant:"""


for hint_number in range(1, 11):
    # --------------------------------------------------------------
    # Add next hint to the conversation
    # --------------------------------------------------------------
    task_data = get_task_info_from_token(task_token, enable_printing=False)
    if 'hint' in task_data:
        hint = task_data['hint']
    else:
        print("#"*50,"\nToken is not active anyomore")
        break

    human_message = f"Hint{hint_number}: {hint}"
    print("Human:", human_message)

    # --------------------------------------------------------------
    # Get model answer (it's automaticaly saved to memory)
    # --------------------------------------------------------------
    response = conversation.predict(input=human_message)
    print("AI: ", response)

    if response != "NEXT":
        print("#" * 50)
        print(f"AFTER {hint_number} HINTS WE HAVE THE RESPONSE !\n", response)
        break

data = {"answer": response}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)
