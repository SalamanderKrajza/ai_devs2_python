from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from helpers import get_vector_store

query = "Do you know the name of Adam's dog?"

# --------------------------------------------------------------
# Get related documents by similarity search
# --------------------------------------------------------------
vector_store = get_vector_store()
context = vector_store.similarity_search_with_score(query, k=1)
context_document, context_score = context[0] #Extract 1st document and its score


chat = ChatOpenAI()
response = chat.invoke([
    SystemMessage(f"""
        Answer questions as truthfully using the context below and nothing more. If you don't know the answer, say "don't know".
        context###{context_document.page_content if context else ''}###
    """),
    HumanMessage(query),
])

print(response.content)
