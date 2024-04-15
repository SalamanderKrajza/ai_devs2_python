#############################################################################
# ------------- FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################
# The process is SIMILAR to one described in api_tasks/C04L04/C04L04_README.md
# The API that is preparing answer is in api_tasks/C04L05/C04L05_FLASKAPI.py
# The course task_functions to point api adress are in api_tasks/C04L05_ownapipro.py
#############################################################################
# /------------- /FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################

# --------------------------------------------------------------
# Define model and conversation chain
# --------------------------------------------------------------
# This time we are defining model outside get_response function to initialize it with memory
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = ChatOpenAI()

# ConversationChain automaticaly appends every message to Memory
# In other words every time user is sending requests model sees all previous messages
conversation = ConversationChain(
    llm=chat, verbose=True, memory=ConversationBufferMemory()
)


# --------------------------------------------------------------
# Define function to generate response for user requset
# --------------------------------------------------------------
def get_response_to_user_request(question):
    response = conversation.predict(input=question)
    return(response)

# --------------------------------------------------------------
# Create flask app
# --------------------------------------------------------------
from flask import Flask, request
app = Flask(__name__)

# --------------------------------------------------------------
# Define available methods and route
# --------------------------------------------------------------
@app.route('/', methods=['POST'])
def generate_response_to_user_question():
    if request.method == 'POST':
        # Get user question
        print("Request JSON data:", request.json)
        print("User question is: ", request.json['question'])

        # Generate answer
        answer = get_response_to_user_request(question=request.json['question'])
        print("Answer to user question is", answer)
        formatted_answer = {"reply":answer}
    return formatted_answer

# --------------------------------------------------------------
# Start app
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(port=5000)
