from rag.chunking.preprocessor import clean_text

sample_text = """
This   agreement!!!

shall terminate@@@ within 30 days.
"""

cleaned = clean_text(sample_text)

print("\nCleaned Text:\n")
print(cleaned)