from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import json

# --------------------------------------------------------------
# helpers.ts content
# --------------------------------------------------------------
def parseFunctionCall(result):
    if result.additional_kwargs and "function_call" in result.additional_kwargs:
        return {
            "name": result.additional_kwargs["function_call"]["name"],
            "args": json.loads(result.additional_kwargs["function_call"]["arguments"]),
        }
    return None

# --------------------------------------------------------------
# schema.ts content
# --------------------------------------------------------------
intentSchema = {
    "name": "describe_intention",
    "description": "Describe Adam's intention towards Alice, based on his latest message and details from summary of their conversation.",
    "parameters": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": """
                  Type has to be set to either:
                  'query' — when Alice has to speak, write sth, translate, correct, help, simply answer to Adam's question or access her long-term memory or notes. Should be picked by default and for common conversations and chit-chat.
                  'action' — when Adam asks Alice explicitly to perform an action that she needs to do herself related to Internet connection to the external apps, services, APIs, models (like Wolfram Alpha) finding sth on a website, calculating, giving environment related info (like weather or nearest locations) accessing and reading websites/urls contents, listing tasks, and events and memorizing something by Alice.
                  """,
            }
        },
        "required": ["name"],
    },
}

# --------------------------------------------------------------
# 28.ts content
# --------------------------------------------------------------
model = ChatOpenAI(model_name="gpt-4-0613").bind(functions=[intentSchema])
result = model.invoke([
    HumanMessage(content="Add to my tasks that I need to finish a lesson for AI_Devs course.")
])

action = parseFunctionCall(result)
print(action)
