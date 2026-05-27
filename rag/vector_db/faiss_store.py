import faiss
import numpy as np
import pickle
import os

from rag.retrieval.bm25_retriever import (
    build_bm25_index,
    bm25_search
)


# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

dimension = 384

index = faiss.IndexFlatIP(
    dimension
)

metadata_store = []


# ---------------------------------------------------------
# Add Embedding
# ---------------------------------------------------------

def add_embedding(
    embedding,
    metadata
):

    global index
    global metadata_store

    vector = np.array(

        embedding,

        dtype=np.float32

    ).reshape(1, -1)

    index.add(vector)

    metadata_store.append(
        metadata
    )


# ---------------------------------------------------------
# Hybrid Search
# ---------------------------------------------------------

def hybrid_search(

    query,
    query_embedding,
    top_k=5,
    semantic_weight=0.60,
    lexical_weight=0.40 
):

    global index
    global metadata_store

    # -----------------------------------------------------
    # Semantic Search
    # -----------------------------------------------------

    vector = np.array(

        query_embedding,

        dtype=np.float32

    ).reshape(1, -1)

    distances, indices = index.search(
        vector,
        top_k * 3
    )

    semantic_results = []

    for position, idx in enumerate(
        indices[0]
    ):

        if idx < len(metadata_store):

            result = (
                metadata_store[idx]
                .copy()
            )

            result["semantic_score"] = float(
                distances[0][position]
            )

            semantic_results.append(
                result
            )

    # -----------------------------------------------------
    # BM25 Search
    # -----------------------------------------------------

    lexical_results = bm25_search(

        query,

        metadata_store,

        top_k=top_k * 3
    )

    # -----------------------------------------------------
    # Fusion
    # -----------------------------------------------------

    combined_results = {}

    # Semantic contribution
    for result in semantic_results:

        key = result["text"]

        combined_results[key] = {

            **result,

            "fusion_score":
                result["semantic_score"]
                * semantic_weight
        }

    # Lexical contribution
    for result in lexical_results:

        key = result["text"]

        bm25_score = (
            result["bm25_score"]
        )

        if key not in combined_results:

            combined_results[key] = {

                **result,

                "semantic_score": 0,

                "fusion_score":
                    bm25_score
                    * lexical_weight
            }

        else:

            combined_results[key][
                "fusion_score"
            ] += (

                bm25_score
                * lexical_weight
            )

        combined_results[key][
            "bm25_score"
        ] = bm25_score
        
    # -----------------------------------------------------
    # Normalize Fusion Scores
    # -----------------------------------------------------

    max_fusion = max(

        item["fusion_score"]

        for item in combined_results.values()
    )

    if max_fusion > 0:

        for item in combined_results.values():

            item["fusion_score"] = round(

                item["fusion_score"]
                /
                max_fusion,

                4
            )
    # -----------------------------------------------------
    # Final Sorting
    # -----------------------------------------------------

    final_results = sorted(

        combined_results.values(),

        key=lambda x:
        x["fusion_score"],

        reverse=True
    )

    return final_results[:top_k]


# ---------------------------------------------------------
# Save Index
# ---------------------------------------------------------

def save_index():

    os.makedirs(
        "data/vector_store",
        exist_ok=True
    )

    faiss.write_index(

        index,

        "data/vector_store/faiss.index"
    )

    with open(

        "data/vector_store/metadata.pkl",

        "wb"

    ) as f:

        pickle.dump(
            metadata_store,
            f
        )

    print(
        "\nFAISS index saved successfully!"
    )


# ---------------------------------------------------------
# Load Index
# ---------------------------------------------------------

def load_index():

    global index
    global metadata_store

    index = faiss.read_index(
        "data/vector_store/faiss.index"
    )

    with open(

        "data/vector_store/metadata.pkl",

        "rb"

    ) as f:

        metadata_store = pickle.load(f)

    # Build BM25
    build_bm25_index(
        metadata_store
    )

    print(
        "\nFAISS + BM25 loaded successfully!"
    )