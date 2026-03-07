# src/endee_client.py

import requests
import msgpack
from src.config import ENDEE_BASE_URL, ENDEE_INDEX_NAME


def insert_vector(vector_id, embedding, metadata):
    url = f"{ENDEE_BASE_URL}/api/v1/index/{ENDEE_INDEX_NAME}/vector/insert"

    payload = [
        {
            "id": vector_id,
            "vector": embedding,
            "meta": metadata
        }
    ]

    response = requests.post(url, json=payload)

    print("Insert status:", response.status_code)


def search_vector(query_embedding, top_k=3):
    url = f"{ENDEE_BASE_URL}/api/v1/index/{ENDEE_INDEX_NAME}/search"

    payload = {
        "vector": query_embedding,
        "k": top_k
    }

    response = requests.post(url, json=payload)

    print("Search status:", response.status_code)

    if response.status_code != 200:
        print("Search error:", response.text)
        return None

    # Endee returns MessagePack binary
    try:
        results = msgpack.unpackb(response.content, raw=False)
        print("Decoded search response:", results)
        return results
    except Exception as e:
        print("Failed to decode search:", e)
        return None