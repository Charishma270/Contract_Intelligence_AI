import os

from pdf2image import convert_from_path
import pytesseract

from ocr.preprocessing.text_preprocessing import (
    clean_text
)

from ocr.chunking.chunking import (
    chunk_text
)

from ocr.metadata.metadata_builder import (
    create_metadata
)

from rag.retrieval.embedder import (
    generate_embedding
)

from rag.vector_db.faiss_store import (
    add_embedding,
    save_index
)


# ---------------------------------------------------------
# OCR Config
# ---------------------------------------------------------

POPPLER_PATH = (
    r"C:\poppler"
    r"\Library\bin"
)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ---------------------------------------------------------
# Main OCR + RAG Ingestion Pipeline
# ---------------------------------------------------------

def process_contract(

    pdf_path,
    contract_id="C001"
):

    if not os.path.exists(pdf_path):

        print("❌ PDF not found")

        return []

    # -----------------------------------------------------
    # Convert PDF to Images
    # -----------------------------------------------------

    images = convert_from_path(

        pdf_path,

        poppler_path=POPPLER_PATH
    )

    all_chunks = []

    chunk_counter = 0

    # -----------------------------------------------------
    # Process Each Page
    # -----------------------------------------------------

    for page_num, img in enumerate(

        images,

        start=1
    ):

        print(
            f"Processing page {page_num}..."
        )

        # OCR Extraction
        raw_text = (
            pytesseract.image_to_string(img)
        )

        # Text Cleaning
        cleaned_text = clean_text(
            raw_text
        )

        # Skip empty pages
        if len(cleaned_text.strip()) == 0:

            continue

        # Chunking
        chunks = chunk_text(
            cleaned_text
        )

        # -------------------------------------------------
        # Process Each Chunk
        # -------------------------------------------------

        for chunk in chunks:

            chunk_id = (
                f"chunk_{chunk_counter}"
            )

            # Metadata
            metadata = create_metadata(

                contract_id,

                page_num,

                chunk_id,

                chunk,

                pdf_path
            )

            # -------------------------------------------------
            # Add default fields required by RAG pipeline
            # -------------------------------------------------

            metadata["label_name"] = (
                "Uploaded Contract"
            )

            metadata["target"] = 0

            metadata["text"] = chunk

            # -------------------------------------------------
            # Generate Embedding
            # -------------------------------------------------

            embedding = generate_embedding(
                chunk
            )

            # -------------------------------------------------
            # Store in FAISS
            # -------------------------------------------------

            add_embedding(

                embedding,

                metadata
            )

            all_chunks.append(metadata)

            chunk_counter += 1

    # -----------------------------------------------------
    # Persist FAISS Index
    # -----------------------------------------------------

    save_index()

    print(
        "\n✅ OCR + RAG ingestion completed!"
    )

    print(
        f"Total chunks indexed: "
        f"{len(all_chunks)}"
    )

    return all_chunks


# ---------------------------------------------------------
# Standalone Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_path = "uploads/sample.pdf"

    data = process_contract(
        sample_path
    )

    print(
        "\n✅ Total chunks:",
        len(data)
    )

    if data:

        print(
            "\n🔍 Sample Output:"
        )

        print(data[0])