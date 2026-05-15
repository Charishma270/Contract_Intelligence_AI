import pandas as pd

from rag.chunking.preprocessor import clean_text
from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import (
    add_embedding,
    search_embedding
)

# Load dataset
df = pd.read_csv("data/processed/clause_classification_dataset.csv")

print("\nLoading and indexing legal clauses...\n")

# Store clauses into FAISS
for index, row in df.iterrows():

    text = str(row["text"])

    cleaned_text = clean_text(text)

    if cleaned_text.strip() == "":
        continue

    embedding = generate_embedding(cleaned_text)

    add_embedding(embedding, cleaned_text)

# User query
query = "termination clause"

print(f"\nUser Query: {query}\n")

# Generate query embedding
query_embedding = generate_embedding(query)

# Search similar clauses
results = search_embedding(query_embedding)

print("\nTop Retrieved Legal Clauses:\n")

# Remove duplicates
unique_results = list(set(results))

# Print results
for result in results:

    print(f"Label: {result['label_name']}")
    print(f"Target: {result['target']}")
    print(f"Score: {result['score']:.4f}")

    print("\nClause:\n")
    print(result["text"])

    print("\n" + "-" * 80 + "\n")
    
