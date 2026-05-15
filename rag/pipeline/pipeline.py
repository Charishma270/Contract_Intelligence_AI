# rag/pipeline/pipeline.py

from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    load_index,
    search_embedding
)

from risk_engine.analysis.classifier_inference import (
    classify_clause
)

from risk_engine.scoring.risk_rules import (
    calculate_risk
)


def run_pipeline(query):

    print("\nLoading FAISS index...\n")

    # Load FAISS index
    load_index()

    print(f"\nUser Query: {query}\n")

    # Generate query embedding
    query_embedding = generate_embedding(query)

    print("Embedding Shape:", query_embedding.shape)

    # Semantic retrieval
    results = search_embedding(
        query_embedding,
        top_k=5
    )

    print("\nTop Retrieved Legal Clauses:\n")

    # No results case
    if len(results) == 0:
        print("No matching clauses found.")
        return

    # Track duplicate clauses
    seen_clauses = set()

    # Process retrieved clauses
    for index, result in enumerate(results, start=1):

        clause_text = result["text"]

        # Skip duplicate clauses
        if clause_text in seen_clauses:
            continue

        seen_clauses.add(clause_text)

        # Classify clause
        predicted_label = classify_clause(
            clause_text
        )

        # Calculate risk level
        risk_level = calculate_risk(
            predicted_label
        )

        # Display formatted output
        print(f"\nRESULT #{index}")
        print("=" * 80)

        print(f"Retrieved Label : {result['label_name']}")
        print(f"Predicted Label : {predicted_label}")

        print(f"Risk Level      : {risk_level}")

        print(f"Target          : {result['target']}")
        print(f"Similarity Score: {result['score']:.4f}")

        print("\nClause:\n")
        print(clause_text[:500] + "...")

        print("\n" + "-" * 80)


# Run pipeline
if __name__ == "__main__":

    user_query = "contract termination"

    run_pipeline(user_query)