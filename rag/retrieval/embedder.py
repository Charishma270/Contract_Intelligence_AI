from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    return np.array(
        embedding,
        dtype=np.float32
    )