import json
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

def split_by_tokens(text, max_tokens=500):
    """
    text - text to split into smaller documents
    max_tokens - maximum tokens for each document

    Function is spliting document by following steps
    1. Spliting text into chunks by all double newlines
    2. Create ampty string for new document
    3. Calculate len of created document with additional chunk
    - If document+chunk is not > max_tokens then append chunk and repeat step 3
    - If document+chunk is > than append document to list of documents,
    and create new document with this chunk only
    4. Repeat step 3 until all chunks processed
    """
    def get_tokens_cnt(model_name="gpt-4", messages=[]):
        model = ChatOpenAI(model_name=model_name)
        num_tokens = model.get_num_tokens_from_messages(messages)
        # print(f"Wyliczone tokeny wg LangChain: {num_tokens}")
        return num_tokens
    
    documents = []
    document = ""
    for chunk in text.split("\n\n"):

        tokens = get_tokens_cnt(model_name="gpt-4", messages=[HumanMessage(document + chunk)])
        # print(tokens)
        if tokens > max_tokens:
            documents.append(document)
            document = chunk
        else:
            document += " " + chunk
    if document:
        documents.append(document)

    return documents

def parse_function_call(fragment):    
    try:
        fragment_object = fragment.generations[0][0].dict()
        function_call_data = fragment_object['message']['additional_kwargs']['function_call']
        function_name = function_call_data['name']
        args = json.loads(function_call_data['arguments'])
        args
        return function_name, args
        
    except:
        return None, None

def summarization(content, **kwargs):
    """Extracting text to save to markdown from args generated by model"""
    return content