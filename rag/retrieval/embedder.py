from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cuda"
)

def generate_embedding(text):
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding