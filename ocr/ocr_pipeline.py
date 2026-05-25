import os
from pdf2image import convert_from_path
import pytesseract

from preprocessing.text_preprocessing import clean_text
from chunking.chunking import chunk_text
from metadata.metadata_builder import create_metadata

# ✅ FIX THESE PATHS (VERY IMPORTANT)
POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def process_contract(pdf_path, contract_id="C001"):
    if not os.path.exists(pdf_path):
        print("❌ PDF not found")
        return []

    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

    all_chunks = []
    chunk_counter = 0

    for page_num, img in enumerate(images, start=1):
        print(f"Processing page {page_num}...")

        raw_text = pytesseract.image_to_string(img)

        # ✅ Clean text
        cleaned = clean_text(raw_text)

        # ✅ Chunk text
        chunks = chunk_text(cleaned)

        for chunk in chunks:
            chunk_id = f"chunk_{chunk_counter}"

            metadata = create_metadata(
                contract_id,
                page_num,
                chunk_id,
                chunk,
                pdf_path
            )

            all_chunks.append(metadata)
            chunk_counter += 1

    return all_chunks


if __name__ == "__main__":
    sample_path = "uploads/sample.pdf"

    data = process_contract(sample_path)

    print("\n✅ Total chunks:", len(data))

    if data:
        print("\n🔍 Sample Output:")
        print(data[0])