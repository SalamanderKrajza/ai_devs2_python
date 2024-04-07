import sys
sys.path.append(r'..')
from task_handler import get_task_token, get_task_info_from_token, send_answer_by_task_token, apikey

# --------------------------------------------------------------
# Get task data
# --------------------------------------------------------------
task_token = get_task_token(taskname='search', apikey=apikey)
task_data = get_task_info_from_token(task_token)
import json
print(json.dumps(task_data, indent=4, ensure_ascii=False))
question = task_data['question']

# --------------------------------------------------------------
# Get the data
# --------------------------------------------------------------
import requests
import time

url = "https://unknow.news/archiwum_aidevs.json"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
response = requests.get(url, headers=headers)

content = json.loads(response.text)

#############################################################################
# ------------- Inedex data in qdrant
#############################################################################
from langchain.document_loaders import TextLoader

from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from qdrant_client import QdrantClient
import json
# --------------------------------------------------------------
# Connect to Qdrant and get "ai_devs_search_task" collection info
# --------------------------------------------------------------
COLLECTION_NAME = "ai_devs_search_task"

qdrant = QdrantClient()
embeddings = OpenAIEmbeddings()
result = qdrant.get_collections()
indexed = next((collection for collection in result.collections if collection.name == COLLECTION_NAME), None)
print(result)

# Create collection if not exists
if not indexed:
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"size": 1536, "distance": "Cosine", "on_disk": True},
    )

collection_info = qdrant.get_collection(collection_name=COLLECTION_NAME)
# json.loads(collection_info.json())

# --------------------------------------------------------------
# Convert content from url to Documents with embeddings and index them
# --------------------------------------------------------------
from langchain.docstore.document import Document
if not collection_info.points_count:
    
    # Create Documents with data and metadata
    documents = []
    for element in content:
        document = Document(page_content=element['info'])
        document.metadata["title"] = element['title']
        document.metadata["url"] = element['url']
        document.metadata["date"] = element['date']
        document.metadata["info"] = element['info']
        document.metadata["source"] = COLLECTION_NAME
        document.metadata["uuid"] = str(uuid4())
        documents.append(document)

    # Generate embeddings
    points = []
    for document in documents:
        embedding = embeddings.embed_documents([document.page_content])[0]
        points.append(
            {
                "id": document.metadata["uuid"],
                "payload": document.metadata,
                "vector": embedding,
            }
        )

    # Index
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points,
    )


# --------------------------------------------------------------
# Search documents related to query in selected COLLECTION
# --------------------------------------------------------------
query_embedding = embeddings.embed_query(question)

search_result = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding,
    limit=1,
    query_filter={"must": [{"key": "source", "match": {"value": COLLECTION_NAME}}]},
)

print(question)
for result in search_result:
    print("ID: ", result.id)
    print("Score: ", result.score)
    print(json.dumps(result.payload, indent=4, ensure_ascii=False))


# --------------------------------------------------------------
# Prepare answer
# --------------------------------------------------------------
# The task goal was to get URL relqted to user question
data = {"answer": result.payload['url']}

# --------------------------------------------------------------
# send answer
# --------------------------------------------------------------
response = send_answer_by_task_token(task_token, data)



