from collections import Counter

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
# Dynamic Explainability
# ---------------------------------------------------------

def generate_explanation(

    semantic_score,
    bert_confidence,
    keyword_score,
    disagreement
):

    if disagreement:

        return (
            "Semantic retrieval was strong but "
            "prediction models disagreed."
        )

    elif keyword_score < 0.20:

        return (
            "Low keyword overlap reduced "
            "retrieval confidence."
        )

    elif semantic_score > 0.75:

        return (
            "High semantic similarity improved "
            "retrieval confidence."
        )

    elif bert_confidence > 0.90:

        return (
            "Legal-BERT produced a highly "
            "confident prediction."
        )

    else:

        return (
            "Prediction generated using "
            "hybrid retrieval heuristics."
        )


# ---------------------------------------------------------
# Contract Summary Builder
# ---------------------------------------------------------

def build_contract_summary(results):

    if len(results) == 0:

        return {
            "overall_risk": "Unknown",
            "top_detected_labels": [],
            "high_confidence_clauses": 0
        }

    risk_levels = [
        result["risk_level"]
        for result in results
    ]

    risk_counter = Counter(risk_levels)

    overall_risk = risk_counter.most_common(1)[0][0]

    labels = [
        result["legal_bert_prediction"]
        for result in results
    ]

    top_labels = [
        label
        for label, _ in Counter(labels).most_common(3)
    ]

    high_confidence_count = sum(
        result["final_confidence"] >= 0.80
        for result in results
    )

    return {

        "overall_risk": overall_risk,

        "top_detected_labels": top_labels,

        "high_confidence_clauses": (
            high_confidence_count
        )
    }


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

    # Semantic Retrieval
    results = search_embedding(
        query_embedding,
        top_k=TOP_K
    )

    print("\nTop Retrieved Legal Clauses:\n")

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

        print(
            "Semantic Score:",
            round(result["score"], 4)
        )

        # Skip extremely weak semantic matches
        if result["score"] < 0.35:

            continue

        # Keyword Score
        keyword_score = (
            calculate_keyword_score(
                expanded_keywords,
                clause_text
            )
        )

        # Classical ML prediction
        predicted_label = (
            classify_clause(
                clause_text
            )
        )

        # Legal-BERT prediction
        bert_result = (
            predict_clause_with_legal_bert(
                clause_text
            )
        )

        print(
            "BERT Confidence:",
            round(
                bert_result["confidence"],
                4
            )
        )

        # Skip extremely weak transformer predictions
        if (
            bert_result["confidence"]
            < 0.45
        ):

            continue

        # Multi-label predictions
        multi_labels = (
            predict_multilabel_legal_bert(
                clause_text
            )
        )

        # Detect disagreement
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

        # Disagreement penalty
        if model_disagreement:

            final_confidence -= 0.08

        # Strong keyword bonus
        if keyword_score >= 0.80:

            final_confidence += 0.05

        # Clamp confidence
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
        # Retrieval Reranking Score
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

        # -------------------------------------------------
        # Query-Aware Boosting
        # -------------------------------------------------
        query_lower = query.lower()

        if "termination" in query_lower:

            if result["label_name"] in [

                "Termination For Convenience",

                "Renewal Term",

                "Post-Termination Services"
            ]:

                rerank_score += 0.15

        if "liability" in query_lower:

            if result["label_name"] in [

                "Cap On Liability",

                "Uncapped Liability"
            ]:

                rerank_score += 0.15

        if "renewal" in query_lower:

            if result["label_name"] in [

                "Renewal Term",

                "Notice Period To Terminate Renewal"
            ]:

                rerank_score += 0.15

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
        # Weak Prediction Detection
        # -------------------------------------------------
        weak_prediction = (

            final_confidence < 0.65

            or

            keyword_score < 0.20

            or

            result["score"] < 0.40
        )

        # -------------------------------------------------
        # Risk Scoring
        # -------------------------------------------------
        risk_level = (
            calculate_risk(
                bert_result["prediction"]
            )
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
        # Structured Backend Response
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

            "risk_score": round(
                final_confidence * 100,
                2
            ),

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

        # Store result
        pipeline_results.append(
            structured_result
        )

        # -------------------------------------------------
        # Terminal Output
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

    # -----------------------------------------------------
    # Contract Summary
    # -----------------------------------------------------
    contract_summary = build_contract_summary(
        pipeline_results
    )

    print("\nCONTRACT SUMMARY")

    print("=" * 80)

    print(
        f"Overall Risk : "
        f"{contract_summary['overall_risk']}"
    )

    print(
        f"Top Labels : "
        f"{contract_summary['top_detected_labels']}"
    )

    print(
        f"High Confidence Clauses : "
        f"{contract_summary['high_confidence_clauses']}"
    )

    return {

        "summary": contract_summary,

        "results": pipeline_results
    }


# ---------------------------------------------------------
# Run Pipeline
# ---------------------------------------------------------

if __name__ == "__main__":

    user_query = "termination clause"

    output = run_pipeline(user_query)

    print(output)
