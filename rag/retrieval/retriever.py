from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import add_embedding, search_embedding
from rag.chunking.chunker import chunk_text
from rag.chunking.preprocessor import clean_text

# Sample contract text
sample_contract = """
This   agreement may terminate with 30 days notice!!!

Confidential information must not be shared@@@

Unlimited liability applies to damages.

Payment must be completed within 15 days.

The client may renew the agreement annually.
"""

# Clean contract text
cleaned_contract = clean_text(sample_contract)

# Generate chunks automatically
chunks = chunk_text(cleaned_contract, chunk_size=8)

# Store embeddings in FAISS
for chunk in chunks:
    embedding = generate_embedding(chunk)
    add_embedding(embedding, chunk)

# User query
query = "termination clause"

# Generate query embedding
query_embedding = generate_embedding(query)

# Retrieve most relevant chunks
results = search_embedding(query_embedding)

print("\nTop Retrieved Chunks:\n")

for result in results:
    print(result)