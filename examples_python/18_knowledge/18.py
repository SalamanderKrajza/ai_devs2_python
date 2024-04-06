from langchain.document_loaders import TextLoader
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from search import search_docs

loader = TextLoader("knowledge.md")
doc = loader.load()[0]
documents = [Document(page_content=content) for content in doc.page_content.split("\n\n")]

query = "Can you write me a function that will generate random number in range for easy_?"
filtered = search_docs(documents, query.split(' '))

chat = ChatOpenAI()
result = chat([
    SystemMessage(content=f"""Answer questions as truthfully using the context below and nothing more. If you don't know the answer, say "don't know". 
    
    context### 
    {' '.join(doc.page_content for doc in filtered)} 
    ###"""),
    HumanMessage(content=query),
])

print(result.content)
