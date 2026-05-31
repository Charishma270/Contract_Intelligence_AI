from collections import Counter
import re

from rag.retrieval.embedder import (
    generate_embedding
)

from rag.vector_db.faiss_store import (
    load_index,
    hybrid_search
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

from risk_engine.scoring.risk_calculator import (
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
        "auto renewal",
        "renewed term",
        "renewal period",
        "contract extension",
        "term extension"
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
# Keyword Density Score
# ---------------------------------------------------------

def calculate_keyword_score(

    expanded_keywords,
    clause_text
):

    clause_lower = clause_text.lower()

    words = re.findall(
        r'\w+',
        clause_lower
    )

    word_counter = Counter(words)

    keyword_score = 0.0

    for keyword in expanded_keywords:

        keyword_tokens = keyword.lower().split()

        keyword_count = sum(
            word_counter[token]
            for token in keyword_tokens
        )

        keyword_score += (
            keyword_count * 0.15
        )

    return round(
        min(keyword_score, 1.0),
        4
    )


# ---------------------------------------------------------
# Clause Length Penalty
# ---------------------------------------------------------

def calculate_length_penalty(
    clause_text
):

    word_count = len(
        clause_text.split()
    )

    if word_count > 900:

        return -0.25

    elif word_count > 700:

        return -0.15

    elif word_count > 500:

        return -0.08

    return 0


# ---------------------------------------------------------
# Dynamic Explainability
# ---------------------------------------------------------

def generate_explanation(

    semantic_score,
    bm25_score,
    bert_confidence,
    keyword_score,
    disagreement
):

    if disagreement:

        return (
            "Semantic retrieval was strong "
            "but prediction models disagreed."
        )

    elif keyword_score >= 0.70:

        return (
            "Strong legal keyword density "
            "improved retrieval precision."
        )

    elif bm25_score >= 2.0:

        return (
            "Lexical retrieval strongly "
            "matched legal terminology."
        )

    elif semantic_score > 0.75:

        return (
            "High semantic similarity "
            "improved retrieval confidence."
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

            "high_confidence_clauses": 0,

            "average_confidence": 0
        }

    risk_levels = [

        result["risk_level"]

        for result in results
    ]

    risk_counter = Counter(
        risk_levels
    )

    overall_risk = (
        risk_counter
        .most_common(1)[0][0]
    )

    labels = [

        result["legal_bert_prediction"]

        for result in results
    ]

    top_labels = [

        label

        for label, _ in (
            Counter(labels)
            .most_common(3)
        )
    ]

    average_confidence = round(

        sum(
            result["final_confidence"]
            for result in results
        )

        /

        len(results),

        4
    )

    high_confidence_count = sum(

        result["final_confidence"] >= 0.80

        for result in results
    )

    return {

        "overall_risk":
            overall_risk,

        "top_detected_labels":
            top_labels,

        "high_confidence_clauses":
            high_confidence_count,

        "average_confidence":
            average_confidence
    }


# ---------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------

def run_pipeline(query):

    print("\nLoading Hybrid Retrieval Engine...\n")

    load_index()

    print(f"\nUser Query: {query}\n")

    expanded_keywords = expand_query(
        query
    )

    print(
        "Expanded Query Keywords:",
        expanded_keywords
    )

    # -----------------------------------------------------
    # Generate Query Embedding
    # -----------------------------------------------------

    query_embedding = generate_embedding(
        query
    )

    print(
        "Embedding Shape:",
        query_embedding.shape
    )

    # -----------------------------------------------------
    # Hybrid Retrieval
    # -----------------------------------------------------

    results = hybrid_search(

        query=query,

        query_embedding=query_embedding,

        top_k=TOP_K
    )

    print(
        "\nTop Retrieved Legal Clauses:\n"
    )

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

        if clause_text in seen_clauses:

            continue

        seen_clauses.add(
            clause_text
        )

        semantic_score = round(
            result.get(
                "semantic_score",
                0
            ),
            4
        )

        bm25_score = round(
            result.get(
                "bm25_score",
                0
            ),
            4
        )

        fusion_score = round(
            result.get(
                "fusion_score",
                0
            ),
            4
        )

        print(
            "Semantic Score:",
            semantic_score
        )

        print(
            "BM25 Score:",
            bm25_score
        )

        print(
            "Fusion Score:",
            fusion_score
        )

        # Skip weak retrievals
        if fusion_score < 0.15:

            continue

        # -------------------------------------------------
        # Keyword Density
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
        # Legal-BERT Prediction
        # -------------------------------------------------

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

        if (
            bert_result["confidence"]
            < 0.45
        ):

            continue

        # -------------------------------------------------
        # Multi-label Predictions
        # -------------------------------------------------

        multi_labels = (
            predict_multilabel_legal_bert(
                clause_text
            )
        )

        multi_labels = (
            multi_labels[:3]
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
        # Length Penalty
        # -------------------------------------------------

        length_penalty = (
            calculate_length_penalty(
                clause_text
            )
        )

        # -------------------------------------------------
        # Weighted Hybrid Confidence
        # -------------------------------------------------

        final_confidence = (

            (
                fusion_score
                * 0.35
            )

            +

            (
                bert_result["confidence"]
                * 0.45
            )

            +

            (
                keyword_score
                * 0.20
            )

            +

            length_penalty
        )

        # Agreement boost
        if (

            predicted_label

            ==

            bert_result["prediction"]
        ):

            final_confidence += 0.06

        # Disagreement penalty
        if model_disagreement:

            final_confidence -= 0.10

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
        # Base Reranking Score
        # -------------------------------------------------

        rerank_score = (

            (
                fusion_score
                * 0.45
            )

            +

            (
                keyword_score
                * 0.30
            )

            +

            (
                bert_result["confidence"]
                * 0.25
            )
        )
        
        # -------------------------------------------------
        # Dynamic Query-Aware Boosting
        # -------------------------------------------------

        query_lower = query.lower()

        # Dynamic scaling based on retrieval quality
        dynamic_boost = (

            (
                fusion_score
                * 0.15
            )

            +

            (
                keyword_score
                * 0.10
            )

            +

            (
                bert_result["confidence"]
                * 0.05
            )
        )

        # -------------------------------------------------
        # Termination Queries
        # -------------------------------------------------

        if "termination" in query_lower:

            if result["label_name"] in [

                "Termination For Convenience",

                "Renewal Term",

                "Post-Termination Services",

                "Notice Period To Terminate Renewal"
            ]:

                rerank_score += (
                    dynamic_boost
                )

        # -------------------------------------------------
        # Liability Queries
        # -------------------------------------------------

        if "liability" in query_lower:

            if result["label_name"] in [

                "Cap On Liability",

                "Uncapped Liability",

                "Liquidated Damages"
            ]:

                rerank_score += (
                    dynamic_boost
                )

        # -------------------------------------------------
        # Renewal Queries
        # -------------------------------------------------

        if "renewal" in query_lower:

            if result["label_name"] in [

                "Renewal Term",

                "Notice Period To Terminate Renewal"
            ]:

                rerank_score += (
                    dynamic_boost
                )

        # -------------------------------------------------
        # Payment Queries
        # -------------------------------------------------

        if "payment" in query_lower:

            if result["label_name"] in [

                "Payment Terms",

                "Late Payment Penalty",

                "Invoice Disputes"
            ]:

                rerank_score += (
                    dynamic_boost
                )

        # -------------------------------------------------
        # Confidentiality Queries
        # -------------------------------------------------

        if "confidentiality" in query_lower:

            if result["label_name"] in [

                "Confidentiality",

                "Non-Disclosure",

                "Data Privacy"
            ]:

                rerank_score += (
                    dynamic_boost
                )

        # -------------------------------------------------
        # Normalize Rerank Score
        # -------------------------------------------------

        rerank_score = round(

            min(
                rerank_score,
                1.0
            ),

            4
        )

        # -------------------------------------------------
        # Reliability Band
        # -------------------------------------------------

        if final_confidence >= 0.85:

            reliability_band = (
                "High Confidence"
            )

        elif final_confidence >= 0.65:

            reliability_band = (
                "Moderate Confidence"
            )

        else:

            reliability_band = (
                "Low Confidence"
            )

        # -------------------------------------------------
        # Weak Prediction Detection
        # -------------------------------------------------

        weak_prediction = (

            final_confidence < 0.65

            or

            keyword_score < 0.20

            or

            fusion_score < 0.30
        )

        # -------------------------------------------------
        # Risk Calculation
        # -------------------------------------------------

        risk_level = calculate_risk(
            bert_result["prediction"]
        )


        # -------------------------------------------------
        # Explainability
        # -------------------------------------------------

        explanation = (
            generate_explanation(

                semantic_score,

                bm25_score,

                bert_result["confidence"],

                keyword_score,

                model_disagreement
            )
        )

        # -------------------------------------------------
        # Structured Result
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
                round(
                    final_confidence * 100,
                    2
                ),

            "semantic_score":
                semantic_score,

            "bm25_score":
                bm25_score,

            "fusion_score":
                fusion_score,

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

    print("\nRETRIEVAL ANALYTICS")

    print("=" * 80)

    print(
        f"Total Retrieved Clauses : "
        f"{len(pipeline_results)}"
    )

    if len(pipeline_results) > 0:

        avg_rerank = round(

            sum(
                result["retrieval_rerank_score"]
                for result in pipeline_results
            )

            /

            len(pipeline_results),

            4
        )

        print(
            f"Average Rerank Score : "
            f"{avg_rerank}"
        )

        print(
            f"Average Confidence : "
            f"{contract_summary['average_confidence']}"
        )

    return {

        "summary":
            contract_summary,

        "results":
            pipeline_results
    }


# ---------------------------------------------------------
# Run Pipeline
# ---------------------------------------------------------

if __name__ == "__main__":

    user_query = "termination clause"

    output = run_pipeline(
        user_query
    )

    print(output)