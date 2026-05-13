import pandas as pd

from rag.chunking.preprocessor import clean_text
from rag.retrieval.embedder import generate_embedding
from rag.vector_db.faiss_store import add_embedding

# Load processed dataset
df = pd.read_csv("data/processed/clause_classification_dataset.csv")

print("\nIndexing dataset into FAISS...\n")

# Store embeddings
for index, row in df.iterrows():

    # Get clause text
    text = str(row["text"])

    # Clean text
    cleaned_text = clean_text(text)

    # Skip empty text
    if cleaned_text.strip() == "":
        continue

    # Generate embedding
    embedding = generate_embedding(cleaned_text)

    # Store in FAISS
    add_embedding(embedding, cleaned_text)

    # Progress log
    if index % 100 == 0:
        print(f"Indexed {index} rows")

print("\nFAISS indexing completed successfully!")