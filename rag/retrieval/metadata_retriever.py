from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    load_index,
    search_embedding
)

print("\nLoading FAISS index...\n")

# Load FAISS index
load_index()

# User query
query = "termination clause"

print(f"\nUser Query: {query}\n")

# Generate embedding
query_embedding = generate_embedding(query)

print("Embedding Shape:", query_embedding.shape)

# Search similar clauses
results = search_embedding(
    query_embedding,
    top_k=50,
    label_filter="Termination For Convenience",
    target_filter=1
)

print("\nTop Retrieved Legal Clauses:\n")

# No results case
if len(results) == 0:
    print("No matching clauses found.")

# Display results
for result in results:

    print(f"Label: {result['label_name']}")
    print(f"Target: {result['target']}")
    print(f"Similarity Score: {result['score']:.4f}")

    print("\nClause:\n")
    print(result["text"][:500] + "...")

    print("\n" + "-" * 80 + "\n")