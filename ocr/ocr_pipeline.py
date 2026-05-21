from pdf2image import convert_from_path
import pytesseract
import os

# ✅ Tesseract path (make sure installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(
        pdf_path,
        poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"   # ✅ CORRECT PATH
    )

    full_text = ""

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        full_text += f"\n--- Page {i+1} ---\n{text}"

    return full_text


if __name__ == "__main__":
    sample_path = "uploads/sample.pdf"

    if not os.path.exists(sample_path):
        print("❌ PDF not found")
    else:
        text = extract_text_from_pdf(sample_path)
        print("✅ OCR SUCCESS\n")
        print(text[:1000])