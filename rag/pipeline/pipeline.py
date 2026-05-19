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

from risk_engine.analysis.multi_label_inference import (
    predict_multi_labels
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

        clause_text = result["text"]

        # Skip duplicates
        if clause_text in seen_clauses:

            continue

        seen_clauses.add(clause_text)

        # Skip weak semantic matches
        if result["score"] < 0.65:

            continue

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

        # Multi-label SVM predictions
        multi_labels = predict_multi_labels(
            clause_text
        )

        # Detect disagreement
        model_disagreement = (

            predicted_label
            != bert_result["prediction"]
        )

        # Confidence bands
        if bert_result["confidence"] >= 0.95:

            confidence_band = "Very Strong"

        elif bert_result["confidence"] >= 0.85:

            confidence_band = "Strong"

        else:

            confidence_band = "Moderate"

        # Hybrid confidence score
        final_confidence = round(

            (
                result["score"]
                +
                bert_result["confidence"]
            ) / 2,

            4
        )

        # Reliability bands
        if final_confidence >= 0.85:

            reliability_band = "Highly Reliable"

        elif final_confidence >= 0.70:

            reliability_band = "Reliable"

        else:

            reliability_band = "Needs Review"

        # Weak prediction heuristic
        weak_prediction = (

            final_confidence < 0.70
        )

        # Risk scoring
        risk_level = calculate_risk(
            bert_result["prediction"]
        )

        # Structured backend response
        structured_result = {

            "retrieved_label":
                result["label_name"],

            "classical_prediction":
                predicted_label,

            "legal_bert_prediction":
                bert_result["prediction"],

            "multi_label_predictions":
                multi_labels,

            "risk_level":
                risk_level,

            "semantic_score":
                round(
                    result["score"],
                    4
                ),

            "bert_confidence":
                bert_result["confidence"],

            "bert_confidence_band":
                confidence_band,

            "final_confidence":
                final_confidence,

            "reliability_band":
                reliability_band,

            "model_disagreement":
                model_disagreement,

            "weak_prediction":
                weak_prediction,

            "target":
                result["target"],

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
            f"Classical Prediction : "
            f"{predicted_label}"
        )

        print(
            f"Legal-BERT Prediction : "
            f"{bert_result['prediction']}"
        )

        print(
            f"Multi-Label Predictions : "
            f"{multi_labels}"
        )

        print(
            f"Risk Level : "
            f"{risk_level}"
        )

        print(
            f"Semantic Score : "
            f"{result['score']:.4f}"
        )

        print(
            f"Legal-BERT Confidence : "
            f"{bert_result['confidence']}"
        )

        print(
            f"Final Confidence : "
            f"{final_confidence}"
        )

        print(
            f"Reliability Band : "
            f"{reliability_band}"
        )

        if model_disagreement:

            print(
                "\nMODEL DISAGREEMENT DETECTED"
            )

        if weak_prediction:

            print(
                "\nWEAK PREDICTION — REVIEW ADVISED"
            )

        print("\nClause:\n")

        print(clause_text[:500] + "...")

        print("\n" + "-" * 80)

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