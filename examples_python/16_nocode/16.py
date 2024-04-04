from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from schema import manager_schema
from helper import parse_function_call
import json
import aiohttp

model = ChatOpenAI(
    model_name="gpt-4-0613",
    model_kwargs={"functions": [manager_schema], "function_call": {"name": "task_manager"}}
)

async def todoist(manager):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://hook.eu2.make.com/cplsufoh4efsvzv5gig5vl83nzqdl8y7",
            headers={"Content-Type": "application/json"},
            data=json.dumps(manager["args"])
        ) as response:
            return await response.json()

async def act(command):
    print("User: " + command)
    add = await model.agenerate([
        [SystemMessage(content="Fact: Today is 09/22/2023 20:01."),
         HumanMessage(content=command)]
    ])
    action = parse_function_call(add.generations[0][0].message)
    if action:
        response = await todoist(action)
        data = response["data"]
        print("AI: " + data)
        return data
    return "No action found"

await act("List my tasks")
await act("Buy milk, eggs, and bread this evening, and make a note about the new Alice feature for tmrw mrng")
await act("I bought groceries and finished the newsletter about the new features.")
