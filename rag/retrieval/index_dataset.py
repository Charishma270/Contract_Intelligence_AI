import uuid
import pandas as pd

from rag.chunking.preprocessor import (
    clean_text
)

from rag.chunking.chunker import (
    chunk_text
)

from rag.retrieval.embedder import (
    generate_embedding
)

from rag.vector_db.faiss_store import (
    add_embedding,
    save_index
)


# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

EMBEDDING_MODEL = (
    "all-MiniLM-L6-v2"
)

SOURCE_FILE = (
    "clause_classification_dataset.csv"
)


# ---------------------------------------------------------
# Section Title Extraction
# ---------------------------------------------------------

def extract_section_title(text):

    first_line = (
        text.strip()
        .split("\n")[0]
    )

    if len(first_line) < 80:

        return first_line

    return "Unknown Section"


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

df = pd.read_csv(
    "data/processed/clause_classification_dataset.csv"
)

print(
    "\nIndexing dataset into "
    "Hybrid Retrieval Engine...\n"
)

total_chunks = 0

# ---------------------------------------------------------
# Process Dataset
# ---------------------------------------------------------

for index, row in df.iterrows():

    text = str(
        row["text"]
    )

    cleaned_text = clean_text(
        text
    )

    # Skip empty text
    if cleaned_text.strip() == "":

        continue

    # -----------------------------------------------------
    # Legal-aware chunking
    # -----------------------------------------------------

    chunks = chunk_text(
        cleaned_text
    )

    # -----------------------------------------------------
    # Process chunks
    # -----------------------------------------------------

    for chunk_index, chunk in enumerate(
        chunks
    ):

        chunk = chunk.strip()

        if len(chunk) < 40:

            continue

        # -------------------------------------------------
        # Generate embedding
        # -------------------------------------------------

        embedding = generate_embedding(
            chunk
        )

        # -------------------------------------------------
        # Metadata enrichment
        # -------------------------------------------------

        metadata = {

            "chunk_id":

                str(
                    uuid.uuid4()
                ),

            "chunk_index":

                chunk_index,

            "chunk_length":

                len(
                    chunk.split()
                ),

            "section_title":

                extract_section_title(
                    chunk
                ),

            "source_file":

                SOURCE_FILE,

            "embedding_model":

                EMBEDDING_MODEL,

            "text":

                chunk,

            "label_name":

                row["label_name"],

            "target":

                int(
                    row["target"]
                )
        }

        # -------------------------------------------------
        # Store embedding
        # -------------------------------------------------

        add_embedding(
            embedding,
            metadata
        )

        total_chunks += 1

    # -----------------------------------------------------
    # Progress logging
    # -----------------------------------------------------

    if index % 100 == 0:

        print(
            f"Indexed {index} rows "
            f"| Total Chunks: "
            f"{total_chunks}"
        )

# ---------------------------------------------------------
# Save Retrieval Index
# ---------------------------------------------------------

print(
    "\nSaving Hybrid Retrieval Index...\n"
)

save_index()

print(
    "\nHybrid Retrieval Indexing "
    "completed successfully!"
)

print(
    f"\nTotal Chunks Indexed: "
    f"{total_chunks}"
)