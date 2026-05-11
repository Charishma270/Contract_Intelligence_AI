from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import add_embedding, search_embedding

# Dummy contract chunks
chunks = [
    "This agreement may terminate with 30 days notice.",
    "Confidential information must not be shared.",
    "Unlimited liability applies to damages."
]

# Store embeddings
for chunk in chunks:
    embedding = generate_embedding(chunk)
    add_embedding(embedding, chunk)

# User query
query = "termination clause"

query_embedding = generate_embedding(query)

results = search_embedding(query_embedding)

print("\nTop Retrieved Chunks:\n")

for result in results:
    print(result)