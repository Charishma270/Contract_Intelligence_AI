# rag/pipeline/pipeline.py

from rag.retrieval.embedder import (
    generate_embedding
)

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

from risk_engine.analysis.multilabel_legal_bert_inference import (
    predict_multilabel_legal_bert
)

from risk_engine.scoring.risk_rules import (
    calculate_risk
)


# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

TOP_K = 5


# ---------------------------------------------------------
# Query Expansion Dictionary
# ---------------------------------------------------------

QUERY_EXPANSIONS = {

    "termination": [

        "terminate",

        "termination rights",

        "cancellation",

        "breach",

        "exit clause",

        "end agreement"
    ],

    "liability": [

        "damages",

        "losses",

        "indemnify",

        "claims",

        "legal exposure"
    ],

    "payment": [

        "fees",

        "invoice",

        "compensation",

        "amount due"
    ],

    "confidentiality": [

        "nda",

        "non disclosure",

        "private information",

        "sensitive data"
    ],

    "renewal": [

        "extend",

        "extension",

        "continue",

        "auto renewal"
    ]
}


# ---------------------------------------------------------
# Query Expansion
# ---------------------------------------------------------

def expand_query(query):

    expanded_keywords = []

    query_words = query.lower().split()

    for word in query_words:

        expanded_keywords.append(word)

        if word in QUERY_EXPANSIONS:

            expanded_keywords.extend(
                QUERY_EXPANSIONS[word]
            )

    return list(set(expanded_keywords))


# ---------------------------------------------------------
# Keyword Score
# ---------------------------------------------------------

def calculate_keyword_score(

    expanded_keywords,
    clause_text
):

    clause_lower = (
        clause_text.lower()
    )

    keyword_matches = sum(

        keyword in clause_lower

        for keyword in expanded_keywords
    )

    keyword_score = (

        keyword_matches
        /
        max(len(expanded_keywords), 1)
    )

    return round(keyword_score, 4)


# ---------------------------------------------------------
# Explainability
# ---------------------------------------------------------

def generate_explanation(

    semantic_score,
    bert_confidence,
    keyword_score,
    disagreement
):

    explanation_parts = []

    if semantic_score >= 0.75:

        explanation_parts.append(
            "strong semantic similarity"
        )

    if bert_confidence >= 0.90:

        explanation_parts.append(
            "high Legal-BERT confidence"
        )

    if keyword_score >= 0.30:

        explanation_parts.append(
            "strong keyword overlap"
        )

    if disagreement:

        explanation_parts.append(
            "model disagreement detected"
        )

    if len(explanation_parts) == 0:

        return (
            "Moderate confidence prediction."
        )

    return (
        "Prediction supported by "
        + ", ".join(explanation_parts)
        + "."
    )


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def run_pipeline(query):

    print("\nLoading FAISS index...\n")

    load_index()

    print(f"\nUser Query: {query}\n")

    expanded_keywords = expand_query(
        query
    )

    print(
        "Expanded Query Keywords:",
        expanded_keywords
    )

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

        top_k=TOP_K
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

    pipeline_results = []

    seen_clauses = set()

    # -----------------------------------------------------
    # Process Retrieved Clauses
    # -----------------------------------------------------

    for index, result in enumerate(

        results,

        start=1
    ):

        clause_text = result["text"]

        # Skip duplicates
        if clause_text in seen_clauses:

            continue

        seen_clauses.add(clause_text)

        # Skip weak semantic matches
        if result["score"] < 0.60:

            continue

        # -------------------------------------------------
        # Keyword Score
        # -------------------------------------------------

        keyword_score = (
            calculate_keyword_score(

                expanded_keywords,

                clause_text
            )
        )

        # -------------------------------------------------
        # Classical ML Prediction
        # -------------------------------------------------

        predicted_label = (
            classify_clause(
                clause_text
            )
        )

        # -------------------------------------------------
        # Single-label Legal-BERT
        # -------------------------------------------------

        bert_result = (
            predict_clause_with_legal_bert(
                clause_text
            )
        )

        # Skip weak predictions
        if (
            bert_result["confidence"]
            < 0.75
        ):

            continue

        # -------------------------------------------------
        # Multi-label Legal-BERT
        # -------------------------------------------------

        multi_labels = (
            predict_multilabel_legal_bert(
                clause_text,
                threshold=0.30
            )
        )

        # -------------------------------------------------
        # Model Disagreement
        # -------------------------------------------------

        model_disagreement = (

            predicted_label
            !=
            bert_result["prediction"]
        )

        # -------------------------------------------------
        # Weighted Hybrid Confidence
        # -------------------------------------------------

        final_confidence = (

            (
                result["score"]
                * 0.25
            )

            +

            (
                bert_result["confidence"]
                * 0.65
            )

            +

            (
                keyword_score
                * 0.10
            )
        )

        # Penalty
        if model_disagreement:

            final_confidence -= 0.08

        # Bonus
        if keyword_score >= 0.50:

            final_confidence += 0.05

        final_confidence = max(

            0,

            min(
                round(
                    final_confidence,
                    4
                ),
                1
            )
        )

        # -------------------------------------------------
        # Retrieval Reranking
        # -------------------------------------------------

        rerank_score = (

            (
                result["score"]
                * 0.50
            )

            +

            (
                keyword_score
                * 0.30
            )

            +

            (
                bert_result["confidence"]
                * 0.20
            )
        )

        rerank_score = round(
            rerank_score,
            4
        )

        # -------------------------------------------------
        # Reliability Bands
        # -------------------------------------------------

        if final_confidence >= 0.90:

            reliability_band = (
                "Highly Reliable"
            )

        elif final_confidence >= 0.75:

            reliability_band = (
                "Reliable"
            )

        elif final_confidence >= 0.60:

            reliability_band = (
                "Moderate Confidence"
            )

        else:

            reliability_band = (
                "Needs Review"
            )

        # -------------------------------------------------
        # Weak Prediction Logic
        # -------------------------------------------------

        weak_prediction = (

            final_confidence < 0.65

            or

            keyword_score < 0.15

            or

            result["score"] < 0.65
        )

        # -------------------------------------------------
        # Risk
        # -------------------------------------------------

        risk_level = (
            calculate_risk(
                bert_result["prediction"]
            )
        )

        risk_score = round(
            final_confidence * 100,
            2
        )

        # -------------------------------------------------
        # Explainability
        # -------------------------------------------------

        explanation = (
            generate_explanation(

                semantic_score=
                result["score"],

                bert_confidence=
                bert_result["confidence"],

                keyword_score=
                keyword_score,

                disagreement=
                model_disagreement
            )
        )

        # -------------------------------------------------
        # Final Structured Result
        # -------------------------------------------------

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

            "risk_score":
                risk_score,

            "semantic_score":
                round(
                    result["score"],
                    4
                ),

            "keyword_score":
                keyword_score,

            "bert_confidence":
                bert_result["confidence"],

            "final_confidence":
                final_confidence,

            "retrieval_rerank_score":
                rerank_score,

            "reliability_band":
                reliability_band,

            "model_disagreement":
                model_disagreement,

            "weak_prediction":
                weak_prediction,

            "explanation":
                explanation,

            "target":
                result["target"],

            "clause_text":
                clause_text
        }

        pipeline_results.append(
            structured_result
        )

        # -------------------------------------------------
        # Terminal Display
        # -------------------------------------------------

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
            f"Risk Score : "
            f"{risk_score}"
        )

        print(
            f"Semantic Score : "
            f"{result['score']:.4f}"
        )

        print(
            f"Keyword Score : "
            f"{keyword_score}"
        )

        print(
            f"Final Confidence : "
            f"{final_confidence}"
        )

        print(
            f"Rerank Score : "
            f"{rerank_score}"
        )

        print(
            f"Reliability Band : "
            f"{reliability_band}"
        )

        print(
            f"Explanation : "
            f"{explanation}"
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

        print(
            clause_text[:500]
            + "..."
        )

        print(
            "\n"
            + "-" * 80
        )

    # -----------------------------------------------------
    # Final Sorting
    # -----------------------------------------------------

    pipeline_results = sorted(

        pipeline_results,

        key=lambda x:
        x["retrieval_rerank_score"],

        reverse=True
    )

    return pipeline_results


# ---------------------------------------------------------
# Run Pipeline
# ---------------------------------------------------------

if __name__ == "__main__":

    user_query = (
        "termination clause"
    )

    final_results = run_pipeline(
        user_query
    )

    print(
        "\nPipeline executed successfully!"
    )

    print(
        "\nStructured Output:\n"
    )

    for result in final_results:

        print(result)

        print(
            "\n"
            + "=" * 80
        )