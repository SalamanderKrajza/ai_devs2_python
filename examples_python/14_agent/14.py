# from typing import Dict, Callable
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage
from schema import add_schema, multiply_schema, subtract_schema
from helper import parse_function_call
from datatypes import ITools

model = ChatOpenAI(
    model_name="gpt-4-0613",
    model_kwargs={"functions": [add_schema, multiply_schema, subtract_schema]}
)

result = model([HumanMessage(content="2929590 * 129359")])

tools: ITools = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
}

action = parse_function_call(result)
if action and action["name"] in tools:
    result_value = tools[action["name"]](action["args"]["first"], action["args"]["second"])
    print(f"The result is {result_value}")
else:
    print(result.content)
