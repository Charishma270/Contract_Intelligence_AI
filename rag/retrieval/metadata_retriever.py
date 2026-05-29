from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    load_index,
    search_embedding
)

from risk_engine.analysis.classifier_inference import (
    classify_clause
)

from risk_engine.scoring.risk_calculator import (
    calculate_risk
)

print("\nLoading FAISS index...\n")

# Load FAISS index
load_index()

# User query
query = "termination clause"

print(f"\nUser Query: {query}\n")

# Generate query embedding
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

    # ML classification
    predicted_label = classify_clause(
        result["text"]
    )

    # Risk scoring
    risk_level = calculate_risk(
        predicted_label
    )

    # Output
    print(f"Retrieved Label: {result['label_name']}")
    print(f"Predicted Label: {predicted_label}")

    print(f"Risk Level: {risk_level}")

    print(f"Target: {result['target']}")
    print(f"Similarity Score: {result['score']:.4f}")

    print("\nClause:\n")
    print(result["text"][:500] + "...")

    print("\n" + "-" * 80 + "\n")