import pandas as pd

from rag.chunking.preprocessor import clean_text
from rag.chunking.chunker import chunk_text

from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    add_embedding,
    search_embedding,
    save_index
)

# Load dataset
df = pd.read_csv(
    "data/processed/clause_classification_dataset.csv"
)

print("\nLoading and indexing legal clauses...\n")

# Store clauses into FAISS
for index, row in df.iterrows():

    text = str(row["text"])

    cleaned_text = clean_text(text)

    # Skip empty text
    if cleaned_text.strip() == "":
        continue

    # Create chunks
    chunks = chunk_text(cleaned_text)

    # Process each chunk
    for chunk in chunks:

        embedding = generate_embedding(chunk)

        # Store embedding + metadata
        add_embedding(
            embedding,
            {
                "text": chunk,
                "label_name": row["label_name"],
                "target": int(row["target"])
            }
        )

# Save FAISS index
save_index()

print("\nFAISS indexing completed successfully!")

# User query
query = "termination clause"

print(f"\nUser Query: {query}\n")

# Generate query embedding
query_embedding = generate_embedding(query)

# Search similar clauses
results = search_embedding(
    query_embedding,
    top_k=5
)

print("\nTop Retrieved Legal Clauses:\n")

# Track duplicates
seen_clauses = set()

# Print results
for result in results:

    clause_text = result["text"]

    # Skip duplicates
    if clause_text in seen_clauses:
        continue

    seen_clauses.add(clause_text)

    print(f"Label: {result['label_name']}")
    print(f"Target: {result['target']}")
    print(f"Similarity Score: {result['score']:.4f}")

    print("\nClause:\n")
    print(clause_text[:500] + "...")

    print("\n" + "-" * 80 + "\n")