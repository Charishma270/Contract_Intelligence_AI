import pandas as pd

from rag.chunking.preprocessor import clean_text
from rag.chunking.chunker import chunk_text
from rag.retrieval.embedder import generate_embedding

from rag.vector_db.faiss_store import (
    add_embedding,
    save_index
)



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

    # Split into chunks
    chunks = chunk_text(cleaned_text)

    # Generate embeddings for each chunk
    for chunk in chunks:

        embedding = generate_embedding(chunk)

        add_embedding(
            embedding,
            {
                "text": chunk,
                "label_name": row["label_name"],
                "target": int(row["target"])
            }
        )

    # Progress log
    if index % 100 == 0:
        print(f"Indexed {index} rows")


print("\nFAISS indexing completed successfully!")

save_index()
