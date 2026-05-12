from rag.chunking.chunker import chunk_text

sample_text = """
This agreement may terminate with 30 days notice.
Unlimited liability applies to damages.
Payment must be completed within 15 days.
"""

chunks = chunk_text(sample_text, chunk_size=5)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}:")
    print(chunk)