from langchain.schema import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json
from datetime import datetime

async def rephrase(response: str, query: str) -> str:
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=1,
    )
    content = (await model.agenerate([[
        SystemMessage(content=f"""
            Answer the question ultra-briefly using casual, human-friendly tone: 
            ###{query}###
            and act as if you just performed this action and confirming this fact to the user, using the following response: 
            ###{json.dumps(response)}###
        """),
    ]])).generations[0][0].text

    return content

def parse_function_call(result: BaseMessage):
    if result.additional_kwargs and "function_call" in result.additional_kwargs:
        return {
            "name": result.additional_kwargs["function_call"]["name"],
            "args": json.loads(result.additional_kwargs["function_call"]["arguments"]),
        }
    return None

def current_date() -> str:
    date = datetime.now()

    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday = weekdays[date.weekday()]

    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    year = date.year

    hours = str(date.hour).zfill(2)
    minutes = str(date.minute).zfill(2)

    return f"{weekday}, {month}/{day}/{year} {hours}:{minutes}"
