from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

documents = [
    Document(page_content="Adam is a programmer who specializes in JavaScript full-stack development"),
    Document(page_content="with a particular focus on using frameworks like Svelte and NestJS"),
    Document(page_content="Adam has a dog named Alexa."),
    Document(page_content="Adam is also a designer."),
]

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(documents, embeddings)

result_one = vector_store.similarity_search("What does Adam do?", k=3)
print(result_one)
