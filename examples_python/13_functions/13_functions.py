from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage
import json

query_enrichment_schema = {
    "name": "query_enrichment",
    "description": "Describe users query with semantic tags and classify with type",
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "boolean",
                "description": "Set to 'true' when query is direct command for AI. Set to 'false' when queries asks for saying/writing/translating/explaining something and all other."
            },
            "type": {
                "type": "string",
                "description": "memory (queries about the user and/or AI), notes|links (queries about user's notes|links). By default pick 'memory'.",
                "enum": ["memory", "notes", "links"]
            },
            "tags": {
                "type": "array",
                "description": "Multiple semantic tags/keywords that enriches query for search purposes (similar words, meanings). When query refers to the user, add 'overment' tag, and when refers to 'you' add tag 'Alice'",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [
            "type", "tags", "command"
        ]
    }
}


# --------------------------------------------------------------
# OWN TEST - Example without using funciton_call
# --------------------------------------------------------------
# kwarg function_call is used to selectdefault function that should be used by model
# if skipped we need to suggest model to use it in the user prompt
# if provided then model will call funciton by default
model = ChatOpenAI(
    model_name="gpt-4-0613",
    model_kwargs={
        "functions": [query_enrichment_schema]
        # "function_call": {"name": "query_enrichment"}, 
    }
)

result = model([HumanMessage(content="Hey there!")])
print(json.dumps(json.loads(result.json()), indent=4)) #Returns just normal model greeting

result = model([HumanMessage(content="Describe this query: I just want to say HELLO!")])
print(json.dumps(json.loads(result.json()), indent=4)) #returns desired schema
# --------------------------------------------------------------
# /OWN TEST - Example without using funciton_call
# --------------------------------------------------------------



model = ChatOpenAI(
    model_name="gpt-4-0613",
    model_kwargs={
        "functions": [query_enrichment_schema],
        "function_call": {"name": "query_enrichment"}, 
    }
)

print(json.dumps({
    "functions": [query_enrichment_schema],
    "function_call": {"name": "query_enrichment"},
}, indent=4))

result = model([HumanMessage(content="Hey there!")])

# --------------------------------------------------------------
# extract desired data
# --------------------------------------------------------------
def parse_function_call(result: BaseMessage):
    if result.additional_kwargs and "function_call" in result.additional_kwargs:
        return {
            "name": result.additional_kwargs["function_call"]["name"],
            "args": json.loads(result.additional_kwargs["function_call"]["arguments"]),
        }
    return None

action = parse_function_call(result)
if action:
    print(action["name"], action["args"])


#############################################################################
# ------------- Add part to call the function basing on model response
#############################################################################
possible_functions = {}

def query_enrichment(command, type, tags, **kwargs):
    """
    It should have some connection to database and use formated output
    in some meaningful way, however I am just presenting how we can call function
    by now. Final implementetion is not important here
    """
    print("Command: ", command, "\ntype: ", type, "\nTags: ",tags)
    
possible_functions['query_enrichment'] = query_enrichment

# just for readability
func_name = action["name"]
func_args =  action["args"]

if action and func_name in possible_functions:
    possible_functions[func_name](**func_args)
