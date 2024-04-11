# OWNAPI TASK
This task requires to create API that will answer requests by using LLM to prepare answer to his question.

#### Used files
- **api_tasks/C04L04/C04L04_README.md** - process description 
- **api_tasks/C04L04/C04L04_FLASKAPI.py** - app that is preparing answer
- **api_tasks/C04L04_ownapi.py** - task_functions that points external api to our app (to complete task in course)


# Steps to complete
## Prepare function to generate answers by LLM
```py
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def get_response_to_user_request(question):
    chat = ChatOpenAI(model="gpt-4")
    response = chat.invoke(input=[
        SystemMessage(content="Answer the user question"),
        HumanMessage(content=question)
        ])
    return(response.content)
```

## Prepare flask API that will
1. Catch user request
2. Extract question from json
3. Use get_response_to_user_request function to prepare answer
4. Return answer

```py
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


#Start flask app
if __name__ == '__main__':
    app.run(port=5000)
```

## Start flask app
Just type `python C04L04_FLASKAPI.py` in console, it should display url to your api
for example:  `Running on http://127.0.0.1:5000`

Only POST method was allowed so we can't just open it in web browser

## Using ngrok for Local App Access from internet
#### What is ngrok?
ngrok is a tool that allows others to access your locally running app by creating a public URL that tunnels traffic to your application. This is useful when you don't have a public IP address and want to make your app accessible over the internet.

#### **Step 1: Download ngrok**

Download the ngrok executable (ngrok.exe) from [the official website.](https://ngrok.com/download)

#### **Step 2: Create an ngrok Account and Generate a Token**

- Sign up for an ngrok account on their website.
- Generate an authentication token from your ngrok dashboard.

#### **Step 3: Configure ngrok with Your Token**

- Open a new console window.
- Navigate to the directory where ngrok.exe is located (if ngrok is not added to your system's PATH).
- Run the following command to add your authentication token:

        ngrok config add-authtoken <YOUR_TOKEN>

    Replace <YOUR_TOKEN> with the token you generated in Step 2.

#### **Step 4: Start ngrok Tunnel**

In the same console window, run the following command to start the ngrok tunnel:

    ngrok http http://localhost:5000

Make sure the port number (5000 in this example) matches the port your app is running on (specified in app.run()).

#### **Step 5: Access Your App via the Public URL**

- In the ngrok console, look for the "Forwarding" section.
- Copy the public URL provided by ngrok (e.g., https://xxxxxxxx.ngrok.io).
- Now you can share this with others OR you may pass this url as ANSWER in task /answer endpoint in your C04L04_ownapi.py file

        data = {"answer": <YOUR_URL_ADRESS>}
        response = send_answer_by_task_token(task_token, data)


# Complete the task
Just executing parts of C04L04_ownapi.py while api is running