from langchain.schema import BaseMessage
import json

def parse_function_call(result: BaseMessage):
    if result.additional_kwargs and "function_call" in result.additional_kwargs:
        return {
            "name": result.additional_kwargs["function_call"]["name"],
            "args": json.loads(result.additional_kwargs["function_call"]["arguments"]),
        }
    return None
