##################################################
# ------------- Example4 - using get_numtokens_from_messages
##################################################
from langchain_openai import ChatOpenAI
from langchain.schema import  SystemMessage

model = ChatOpenAI(model_name="gpt-3.5-turbo")

messages = [
    SystemMessage("Cześć, to jest test!")
]

# Calculate number of prompt tokens
num_tokens = model.get_num_tokens_from_messages(messages)
print(f"Wyliczone tokeny wg LangChain: {num_tokens}")

# Test if calculations are correct
response = model.invoke(messages)
tokens_used = response.response_metadata['token_usage']['prompt_tokens']
print(f"Zuzyte tokeny wg LangChain: {tokens_used}")


##################################################
# ------------- Example4 - Tiktoken with library only (not as precise as example from repo)
##################################################
text_to_check = "Cześć, to jest test!"

import tiktoken
encoding = tiktoken.encoding_for_model("gpt-4")
list_of_tokens = encoding.encode(text_to_check)
number_of_tokens = len(list_of_tokens)

print(list_of_tokens, number_of_tokens)


##################################################
# ------------- Example4 - Tiktoken more precise calculations
##################################################
from typing import List, Dict
from tiktoken import get_encoding
import openai
choosen_model = "gpt-4"

def count_tokens(messages: List[Dict[str, str]], model="gpt-3.5-turbo-0613") -> int:
    encoding = get_encoding("cl100k_base")

    tokens_per_message, tokens_per_name = 0, 0

    if model in ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0314", "gpt-4-32k-0314", "gpt-4-0613", "gpt-4-32k-0613"]:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4
        tokens_per_name = -1
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return count_tokens(messages, "gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return count_tokens(messages, "gpt-4-0613")
    else:
        raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3
    return num_tokens

# Przykładowe użycie funkcji count_tokens
messages = [
    {
        "role": "system",
        "content": "Cześć, to jest test!",
    }
]

# Obliczanie liczby tokenów
num = count_tokens(messages, choosen_model)
print("Token Count:", num)

# Kodowanie treści wiadomości na tokeny
encoding = tiktoken.encoding_for_model(choosen_model) #get_encoding("cl100k_base")
print("Token IDs:", encoding.encode(messages[0]["content"]))

# PORÓWNANIE Z WYNIKIEM OPENAI
response = openai.chat.completions.create(
            model=choosen_model,
            messages=messages)
print(f"Zuzyte tokeny wg OpenAI: {response.usage.prompt_tokens}")
