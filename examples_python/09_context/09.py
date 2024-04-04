from dotenv import load_dotenv
import os
load_dotenv()

from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI


loader = TextLoader("memory.md")
doc = loader.load()[0]

chat = ChatOpenAI()
content = chat([
    SystemMessage(content=f"""
        Answer questions as truthfully using the context below and nothing more. If you don't know the answer, say "don't know".
        context###{doc.page_content}###
    """),
    HumanMessage(content="Who is overment?")
])

print(content.content)
