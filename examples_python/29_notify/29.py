from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from helpers import get_vector_store

query = "Write a summary of the games by AI_Devs."

# --------------------------------------------------------------
# Get related documents by similarity search
# --------------------------------------------------------------
vector_store = get_vector_store()
context = vector_store.similarity_search_with_score(query, k=1)
context_document, context_score = context[0] #Extract 1st document and its score


chat = ChatOpenAI()
response = chat.invoke([
    SystemMessage(f"""
  Assign the task provided by the user to the person who is most likely to complete it based on the context and nothing else.
          Return the lowercase name or "general" if you can't find a match.
        context###${context_document.page_content if context else ''}###
    """),
    HumanMessage(query),
])

print("Notify:", response.content)
