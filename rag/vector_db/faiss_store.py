import faiss
import numpy as np

# Create FAISS index
dimension = 384

index = faiss.IndexFlatIP(dimension)

documents = []

def add_embedding(embedding, text):
    vector = np.array([embedding]).astype("float32")
    index.add(vector)
    documents.append(text)

def search_embedding(query_embedding, top_k=2):
    vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(vector, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results