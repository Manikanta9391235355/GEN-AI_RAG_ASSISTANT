import json
from embeddings import generate_embedding
from vector_store import InMemoryVectorStore

store = InMemoryVectorStore()

# 🔥 Lower threshold for realistic retrieval
SIMILARITY_THRESHOLD = 0.60


def load_documents():
    with open("docs.json", "r", encoding="utf-8") as f:
        docs = json.load(f)

    for doc in docs:
        embedding = generate_embedding(doc["content"])
        store.add(embedding, doc)


def retrieve(query):
    query_embedding = generate_embedding(query)

    results = store.search(query_embedding, top_k=3)

    print("\n🔎 Top Similarity Matches:")
    for score, meta in results:
        print(f"{meta['title']} → {round(score, 4)}")

    # Apply threshold
    filtered = [r for r in results if r[0] >= SIMILARITY_THRESHOLD]

    return filtered