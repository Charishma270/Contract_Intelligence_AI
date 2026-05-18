# rag/pipeline/pipeline.py

from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    load_index,
    search_embedding
)

from risk_engine.analysis.classifier_inference import (
    classify_clause
)

from risk_engine.analysis.legal_bert_inference import (
    predict_clause_with_legal_bert
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
        return []

    # Store structured output
    pipeline_results = []

    # Track duplicate clauses
    seen_clauses = set()

    # Process retrieved clauses
    for index, result in enumerate(results, start=1):

        # Skip weak semantic matches
        if result["score"] < 0.68:

            continue

        clause_text = result["text"]

        # Skip duplicate clauses
        if clause_text in seen_clauses:
            continue

        seen_clauses.add(clause_text)

        # Classical ML prediction
        predicted_label = classify_clause(
            clause_text
        )

        # Legal-BERT prediction
        bert_result = predict_clause_with_legal_bert(
            clause_text
        )

        # Skip weak transformer predictions
        if bert_result["confidence"] < 0.75:

            continue

        # Detect disagreement between models
        model_disagreement = (

            predicted_label
            != bert_result["prediction"]
        )

        # Risk scoring based on Legal-BERT
        risk_level = calculate_risk(
            bert_result["prediction"]
        )

        # Weighted hybrid ranking
        hybrid_score = round(

            (
                (0.4 * result["score"])
                +
                (0.6 * bert_result["confidence"])
            ),

            4
        )

        # Build backend-compatible response
        structured_result = {

            "clause_type":
                predicted_label,

            "retrieved_label":
                result["label_name"],

            "risk_level":
                risk_level,

            "similarity_score":
                round(
                    result["score"],
                    4
                ),

            "hybrid_score":
                hybrid_score,

            "target":
                result["target"],

            "legal_bert_prediction":
                bert_result["prediction"],

            "legal_bert_confidence":
                bert_result["confidence"],

            "model_disagreement":
                model_disagreement,

            "clause_text":
                clause_text
        }

        # Store final output
        pipeline_results.append(
            structured_result
        )

        # Terminal display
        print(f"\nRESULT #{index}")
        print("=" * 80)

        print(
            f"Retrieved Label : "
            f"{result['label_name']}"
        )

        print(
            f"Classical ML Prediction : "
            f"{predicted_label}"
        )

        print(
            f"Legal-BERT Prediction : "
            f"{bert_result['prediction']}"
        )

        print(
            f"Legal-BERT Confidence : "
            f"{bert_result['confidence']}"
        )

        print(
            f"Hybrid Score : "
            f"{hybrid_score}"
        )

        print(
            f"Risk Level : "
            f"{risk_level}"
        )

        print(
            f"Target : "
            f"{result['target']}"
        )

        print(
            f"Similarity Score : "
            f"{result['score']:.4f}"
        )

        # Model disagreement warning
        if model_disagreement:

            print(
                "\nMODEL DISAGREEMENT DETECTED"
            )

        print("\nClause:\n")

        print(clause_text[:500] + "...")

        print("\n" + "-" * 80)

    # Sort by weighted hybrid ranking
    pipeline_results = sorted(

        pipeline_results,

        key=lambda x: x["hybrid_score"],

        reverse=True
    )

    # Return structured results
    return pipeline_results


# Run pipeline
if __name__ == "__main__":

    user_query = "contract termination"

    final_results = run_pipeline(
        user_query
    )

    print("\nPipeline executed successfully!")

    print("\nStructured Output:\n")

    for result in final_results:

        print(result)

        print("\n" + "=" * 80)