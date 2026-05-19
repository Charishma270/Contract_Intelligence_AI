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


def calculate_final_confidence(

    semantic_score,
    bert_confidence,
    model_disagreement
):

    # Weighted confidence fusion
    final_score = (

        (semantic_score * 0.4)
        +
        (bert_confidence * 0.6)
    )

    # Penalize disagreement
    if model_disagreement:

        final_score -= 0.10

    # Clamp range
    final_score = max(
        0.0,
        min(final_score, 1.0)
    )

    return round(final_score, 4)


def get_final_decision_band(score):

    if score >= 0.90:
        return "Highly Reliable"

    elif score >= 0.75:
        return "Reliable"

    elif score >= 0.60:
        return "Moderately Reliable"

    return "Low Reliability"


def run_pipeline(query):

    print("\nLoading FAISS index...\n")

    # Load FAISS index
    load_index()

    print(f"\nUser Query: {query}\n")

    # Generate query embedding
    query_embedding = generate_embedding(
        query
    )

    print(
        "Embedding Shape:",
        query_embedding.shape
    )

    # Semantic retrieval
    results = search_embedding(
        query_embedding,
        top_k=5
    )

    print(
        "\nTop Retrieved Legal Clauses:\n"
    )

    # No results
    if len(results) == 0:

        print(
            "No matching clauses found."
        )

        return []

    # Final structured outputs
    pipeline_results = []

    # Duplicate prevention
    seen_clauses = set()

    # Process clauses
    for index, result in enumerate(
        results,
        start=1
    ):

        clause_text = result["text"]

        # Skip duplicates
        if clause_text in seen_clauses:
            continue

        seen_clauses.add(clause_text)

        # Semantic similarity
        semantic_score = round(
            result["score"],
            4
        )

        # Classical ML prediction
        predicted_label = classify_clause(
            clause_text
        )

        # Legal-BERT prediction
        bert_result = (
            predict_clause_with_legal_bert(
                clause_text
            )
        )

        # Detect disagreement
        model_disagreement = (

            predicted_label
            != bert_result["prediction"]
        )

        # Final confidence
        final_confidence = (
            calculate_final_confidence(

                semantic_score,

                bert_result["confidence"],

                model_disagreement
            )
        )

        # Reliability band
        reliability_band = (
            get_final_decision_band(
                final_confidence
            )
        )

        # Risk scoring
        risk_level = calculate_risk(

            bert_result["prediction"]
        )

        # Weak predictions warning
        weak_prediction = (
            final_confidence < 0.60
        )

        # Structured output
        structured_result = {

            "retrieved_label":
                result["label_name"],

            "classical_prediction":
                predicted_label,

            "legal_bert_prediction":
                bert_result["prediction"],

            "risk_level":
                risk_level,

            "semantic_score":
                semantic_score,

            "bert_confidence":
                bert_result["confidence"],

            "bert_confidence_band":
                bert_result[
                    "confidence_band"
                ],

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

        # Store output
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
            f"Risk Level : "
            f"{risk_level}"
        )

        print(
            f"Semantic Score : "
            f"{semantic_score}"
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

        # Disagreement warning
        if model_disagreement:

            print(
                "\nWARNING: "
                "MODEL DISAGREEMENT DETECTED"
            )

        # Weak prediction warning
        if weak_prediction:

            print(
                "\nWARNING: "
                "LOW CONFIDENCE PREDICTION"
            )

        print("\nClause:\n")

        print(
            clause_text[:500] + "..."
        )

        print("\n" + "-" * 80)

    # Sort by final confidence
    pipeline_results = sorted(

        pipeline_results,

        key=lambda x:
            x["final_confidence"],

        reverse=True
    )

    return pipeline_results


# Run pipeline
if __name__ == "__main__":

    user_query = "contract termination"

    final_results = run_pipeline(
        user_query
    )

    print(
        "\nPipeline executed successfully!"
    )

    print("\nStructured Output:\n")

    for result in final_results:

        print(result)

        print("\n" + "=" * 80)