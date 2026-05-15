import pandas as pd

from rag.chunking.preprocessor import clean_text
from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import (
    add_embedding,
    search_embedding
)

# Load dataset
df = pd.read_csv("data/processed/clause_classification_dataset.csv")

print("\nTesting metadata-aware retrieval...\n")

# Index small sample for testing
sample_df = df

for _, row in sample_df.iterrows():

    text = str(row["text"])

    cleaned_text = clean_text(text)

    embedding = generate_embedding(cleaned_text)

    add_embedding(
        embedding,
        {
            "text": cleaned_text,
            "label_name": row["label_name"],
            "target": int(row["target"])
        }
    )

# Test query
query = "liability clause"

query_embedding = generate_embedding(query)

results = search_embedding(query_embedding, top_k=2)

print("\nRetrieved Results:\n")

for result in results:

    print(f"Label: {result['label_name']}")
    print(f"Target: {result['target']}")
    print(f"Score: {result['score']:.4f}")

    print("\nClause:\n")
    print(result["text"])

    print("\n" + "-" * 80 + "\n")