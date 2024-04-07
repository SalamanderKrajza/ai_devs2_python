import os
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document

VECTOR_STORE_PATH = "memory.index"
MEMORY_PATH = "memory.md"

def get_vector_store():
    # --------------------------------------------------------------
    # Create memory.index folder if not exists
    # --------------------------------------------------------------
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(VECTOR_STORE_PATH, embeddings=OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    # --------------------------------------------------------------
    # Load markdown file data to list of Document objects
    # --------------------------------------------------------------
    loader = TextLoader(MEMORY_PATH)
    memory = loader.load()[0]
    documents = [Document(page_content=content) for content in memory.page_content.split("\n\n")]

    # --------------------------------------------------------------
    # Use from_document to convert text to embeddings, create indexes, create FIASS object and save it
    # --------------------------------------------------------------
    # FAISS.from_documents() takes a list of documents and:
    # - generates vector embeddings using OpenAI's embeddings model, 
    # - creates a FAISS vector index, (by default IndexFLatL2)
    # - stores the embeddings and documents in the index
    # - returns a searchable FAISS object.
    store = FAISS.from_documents(documents, OpenAIEmbeddings())
    store.save_local(VECTOR_STORE_PATH)
    return store


