from rank_bm25 import BM25Okapi
import numpy as np


bm25_index = None
bm25_documents = []


# ---------------------------------------------------------
# Build BM25 Index
# ---------------------------------------------------------

def build_bm25_index(metadata_store):

    global bm25_index
    global bm25_documents

    bm25_documents = [

        item["text"].lower().split()

        for item in metadata_store
    ]

    bm25_index = BM25Okapi(
        bm25_documents
    )

    print(
        "\nBM25 index built successfully!"
    )


# ---------------------------------------------------------
# Normalize Scores
# ---------------------------------------------------------

def normalize_scores(scores):

    if len(scores) == 0:

        return scores

    min_score = min(scores)
    max_score = max(scores)

    # Prevent divide-by-zero
    if max_score == min_score:

        return [0.0 for _ in scores]

    normalized = [

        (
            score - min_score
        )

        /

        (
            max_score - min_score
        )

        for score in scores
    ]

    return normalized


# ---------------------------------------------------------
# BM25 Search
# ---------------------------------------------------------

def bm25_search(

    query,
    metadata_store,
    top_k=5
):

    global bm25_index

    if bm25_index is None:

        build_bm25_index(
            metadata_store
        )

    tokenized_query = (
        query.lower().split()
    )

    raw_scores = bm25_index.get_scores(
        tokenized_query
    )

    normalized_scores = (
        normalize_scores(
            raw_scores
        )
    )

    ranked_indices = sorted(

        range(len(normalized_scores)),

        key=lambda i:
        normalized_scores[i],

        reverse=True
    )[:top_k]

    results = []

    for idx in ranked_indices:

        result = metadata_store[idx].copy()

        result["bm25_score"] = round(

            float(
                normalized_scores[idx]
            ),

            4
        )

        results.append(result)

    return results