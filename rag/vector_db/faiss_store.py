import faiss
import numpy as np
import pickle
import os

# Embedding dimension
dimension = 384

# Create FAISS index
index = faiss.IndexFlatIP(dimension)

# Store metadata
metadata_store = []


def add_embedding(embedding, metadata):

    global index
    global metadata_store

    # Ensure correct dtype + shape
    vector = np.array(embedding, dtype=np.float32).reshape(1, -1)

    # Add vector to FAISS
    index.add(vector)

    # Store metadata
    metadata_store.append(metadata)


def search_embedding(
    query_embedding,
    top_k=3,
    label_filter=None,
    target_filter=None
):

    global index
    global metadata_store

    # Ensure correct dtype + shape
    vector = np.array(
        query_embedding,
        dtype=np.float32
    ).reshape(1, -1)

    print("Search Vector Shape:", vector.shape)

    # Search FAISS
    distances, indices = index.search(vector, top_k)

    results = []

    # Retrieve metadata
    for position, idx in enumerate(indices[0]):

        if idx < len(metadata_store):

            result = metadata_store[idx].copy()

            # Apply label filter
            if label_filter is not None:

                if result["label_name"] != label_filter:
                    continue

            # Apply target filter
            if target_filter is not None:

                if result["target"] != target_filter:
                    continue

            # Add similarity score
            result["score"] = float(
                distances[0][position]
            )

            results.append(result)

    return results


# Save FAISS index + metadata
def save_index():

    os.makedirs(
        "data/vector_store",
        exist_ok=True
    )

    # Save FAISS index
    faiss.write_index(
        index,
        "data/vector_store/faiss.index"
    )

    # Save metadata
    with open(
        "data/vector_store/metadata.pkl",
        "wb"
    ) as f:

        pickle.dump(metadata_store, f)

    print("\nFAISS index saved successfully!")


# Load FAISS index + metadata
def load_index():

    global index
    global metadata_store

    # Load FAISS index
    index = faiss.read_index(
        "data/vector_store/faiss.index"
    )

    # Load metadata
    with open(
        "data/vector_store/metadata.pkl",
        "rb"
    ) as f:

        metadata_store = pickle.load(f)

    print("\nFAISS index loaded successfully!")
