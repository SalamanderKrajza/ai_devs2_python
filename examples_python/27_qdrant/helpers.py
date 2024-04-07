#############################################################################
# ------------- Indexing is realized by qdrant.upsert() in main file
#############################################################################

# helpers.py
# import os
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.document_loaders import TextLoader
# from langchain.docstore.document import Document

# VECTOR_STORE_PATH = "21_similarity/memory.index"
# MEMORY_PATH = "21_similarity/memory.md"

# def get_vector_store():
#     if os.path.exists(VECTOR_STORE_PATH):
#         return FAISS.load_local(VECTOR_STORE_PATH, OpenAIEmbeddings())

#     loader = TextLoader(MEMORY_PATH)
#     memory = loader.load()[0]
#     documents = [Document(page_content=content) for content in memory.page_content.split("\n\n")]
#     store = FAISS.from_documents(documents, OpenAIEmbeddings())
#     store.save_local(VECTOR_STORE_PATH)
#     return store
