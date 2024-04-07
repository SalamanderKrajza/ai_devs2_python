from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from qdrant_client import QdrantClient
import json

# REQUIRES TO START DOCKER - docker run -p 6333:6333 qdrant/qdrant

# --------------------------------------------------------------
# Connect to Qdrant and get "ai_devs" collection info
# --------------------------------------------------------------
MEMORY_PATH = "memory.md"
COLLECTION_NAME = "ai_devs"

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

# If no-document is indexed
if not collection_info.points_count:
    # Read File
    loader = TextLoader(MEMORY_PATH)
    memory = loader.load()[0]
    documents = [Document(page_content=content) for content in memory.page_content.split("\n\n")]

    # Add metadata
    for document in documents:
        document.metadata["source"] = COLLECTION_NAME
        document.metadata["content"] = document.page_content
        document.metadata["uuid"] = str(uuid4()) #Generate unique identifier to let us filter this document later

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
query = "Do you know the name of Adam's dog?"
query_embedding = embeddings.embed_query(query)

search_result = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding,
    limit=1,
    query_filter={"must": [{"key": "source", "match": {"value": COLLECTION_NAME}}]},
)

for result in search_result:
    print("ID: ", result.id)
    print("Score: ", result.score)
    print(json.dumps(result.payload,indent=4))