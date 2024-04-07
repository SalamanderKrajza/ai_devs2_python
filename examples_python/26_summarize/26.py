from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import asyncio
from schema import summarization_schema
from prompts import get_prompt
from helpers import parse_function_call, summarization, split_by_tokens
# --------------------------------------------------------------
# Create file object and get the data
# --------------------------------------------------------------
file = {
    "title": "Lekcja kursu AI_Devs, S03L03 — Wyszukiwanie i bazy wektorowe",
    "name": "draft.md",
    "author": "Adam",
    "excerpt": "",
    "content": "",
    "tags": [],
}
summary = {"content": ""}

loader = TextLoader( file["name"], encoding="utf-8")
doc = loader.load()[0]

# --------------------------------------------------------------
# Split text into chunks with maximum 2000 characts length with RecursiveCharacterTextSplitter
# --------------------------------------------------------------
# By default, the separators are ["\n\n", "\n", " ", ""]
# The splitter tries to split the text using a predefined set of separators in a recursive manner. 
# In other words:
# - It splits text into chunks by using "\n\n" separator
# - If (any)chunk_size > 2000 it splits by it "\n"
# - If (any)chunk_size > 2000 it splits by " "
#
# It tries keep semantically related pieces togheter
# Also, we may aenable chunk_overlap to keep fragments of other chunks at begining/end current one
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
documents = text_splitter.split_text(doc.page_content)

# --------------------------------------------------------------
# Alternative split by functions using count tokens
# --------------------------------------------------------------
# This version is more similar to typescript example
documents = split_by_tokens(doc.page_content, max_tokens=500)

# --------------------------------------------------------------
# Create summary
# --------------------------------------------------------------
# NOTE: In course example we are using FUNCITON_CALLING
# However, we not parse anything beside content
# We don't use generated tags or anything
# So it as far as i know - It may be also generated without it
# If you are curious why do we needs "TAGS" args - we don't ;)

semaphore = asyncio.Semaphore(5)  # Limit concurrency to 5

# CREATE MODEL:
# model = ChatOpenAI(model_name="gpt-4") 
model_with_function_calling = ChatOpenAI(model_name="gpt-4",
    model_kwargs={
        "functions": [summarization_schema],
        "function_call": {"name": "summarization"}, 
    },
)

# Define function to get data from api
system_message = get_prompt(file_name = file['name'], file_author = file['author'])
async def summarize(chunk, file) -> str:
    async with semaphore:
        return await model_with_function_calling.agenerate([[
            SystemMessage(content=system_message),
            HumanMessage(content=f"###{chunk}###")
        ]])
    
# Make the api calls
promises = [summarize(doc, file) for doc in documents]
summarised_fragments = await asyncio.gather(*promises)
# single_fragment = json.loads(summarised_fragments[0].json())
# single_fragment['generations'][0][0]['message']['additional_kwargs']['function_call']['arguments']

# --------------------------------------------------------------
# Save outputs to markdown file
# --------------------------------------------------------------
# Create file with header
intro = f"# Summary of the document {file['title']}\n\n"
with open("summarized.md", "w", encoding="utf-8") as f:
    f.write(intro)

# Save summarised fragments to file
for fragment in summarised_fragments:
    func_name, func_args = parse_function_call(fragment)
    if func_name=='summarization':
        content_to_save = summarization(**func_args)
        with open("summarized.md", "a", encoding="utf-8") as f:
            f.write(content_to_save + "\n\n")


