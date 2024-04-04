import json
from langchain.document_loaders import TextLoader
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.schema import HumanMessage, SystemMessage

loader = TextLoader("docs.md")
doc = loader.load()[0]
documents = [Document(page_content=content) for content in doc.page_content.split("\n\n")]
print(documents)

model = ChatOpenAI()

def generate_description(doc):
    return model([
        SystemMessage(content="""
            Describe the following document with one of the following keywords:
            Mateusz, Jakub, Adam. Return the keyword and nothing else.
        """),
        HumanMessage(content=f"Document: {doc.page_content}")
    ]).content

descriptions = []
for doc in documents:
    descriptions.append(generate_description(doc))

for index, description in enumerate(descriptions):
    documents[index].metadata["source"] = description

with open("docs.json", "w") as f:
    json.dump([doc.dict() for doc in documents], f, indent=2)
