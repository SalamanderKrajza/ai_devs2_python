#############################################################################
# ------------- FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################
# The process is described in api_tasks/C04L04/C04L04_README.md
# The API that is preparing answer is in api_tasks/C04L04/C04L04_FLASKAPI.py
# The course task_functions to point api adress are in api_tasks/C04L04_ownapi.py
#############################################################################
# /------------- /FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################

# --------------------------------------------------------------
# Define function to generate response for user requset
# --------------------------------------------------------------
# It will be executed each time someone calls our api
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def get_response_to_user_request(question):
    chat = ChatOpenAI(model="gpt-4")
    response = chat.invoke(input=[
        SystemMessage(content="Answer the user question"),
        HumanMessage(content=question)
        ])
    return(response.content)

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
