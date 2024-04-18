#############################################################################
# ------------- FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################
# The process is SIMILAR to one described in api_tasks/C04L04/C04L04_README.md
# The API that is preparing answer is in api_tasks/C05L03/C05L03_FLASKAPI.py
# The course task_functions to point api adress are in api_tasks/C05L03_google.py
#############################################################################
# /------------- /FOR ANYONE WHO NEEDS ADDITIONAL EXPLANATION OF THIS TASK
#############################################################################
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from serpapi import Client
import os
from dotenv import load_dotenv    
load_dotenv()
apikey = os.environ.get("SERP_API_KEY")

# --------------------------------------------------------------
# Extract keywords for search with llm
# --------------------------------------------------------------
def extract_keywords_from_user_question(question):
    chat = ChatOpenAI()
    response = chat.invoke(input=[
        SystemMessage(content="""You are search assistant that prepare keywords 
                      to search in google from user question
                      
                      Your role is to analyze user question and prepare list of words understandable
                      for google search engine.

                      If user provde website adress to do the search, make sure you will implement it correctly using
                      site:some_website.pl rest of the keywords

                      User will use Polish language and most likely will need polish sources so stick to this language.

                      For example:
                      Q: I don't really remember but I want to know - what is the color of the grass?
                      A: Color of grass
                      Q: Give me url to wikipedia.pl site about unicorns
                      A: site:wikipedia.pl unicorns
                      """),
        HumanMessage(content=question)
        ])
    return(response.content)

# --------------------------------------------------------------
# Do the google search with serpapi lib
# --------------------------------------------------------------
def search_in_google(keywords):
    client = Client(api_key=apikey)
    params = {
    "q": keywords,
    "engine": "google"
    }

    # Get the results
    results = client.search(params)

    # Return 1st url from results
    return results["organic_results"][0]["link"]

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
        print("\nRequest JSON data:", request.json)
        print("User question is: ", request.json['question'])

        # Generate answer
        keywords = extract_keywords_from_user_question(question=request.json['question'])
        print("Extracted keywords are: ", keywords)
        
        answer = search_in_google(keywords=keywords)
        print("Answer to user question is: ", answer)

        formatted_answer = {"reply":answer}
    return formatted_answer

# --------------------------------------------------------------
# Start app
# --------------------------------------------------------------
if __name__ == '__main__':
    app.run(port=5000)