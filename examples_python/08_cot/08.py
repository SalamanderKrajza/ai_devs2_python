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

    