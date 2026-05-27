import re


# ---------------------------------------------------------
# Legal Section Splitter
# ---------------------------------------------------------

def split_legal_sections(text):

    pattern = r'(?=\n?\s*(\d+\.|\([a-z]\)|[A-Z ]{4,}:))'

    sections = re.split(
        pattern,
        text
    )

    cleaned_sections = []

    for section in sections:

        section = section.strip()

        if len(section) > 50:

            cleaned_sections.append(
                section
            )

    return cleaned_sections


# ---------------------------------------------------------
# Smart Chunk Builder
# ---------------------------------------------------------

def build_chunks(

    sections,

    chunk_size=350,

    overlap=75
):

    chunks = []

    current_chunk = ""

    for section in sections:

        # -------------------------------------------------
        # Large section handling
        # -------------------------------------------------

        if len(section.split()) > chunk_size:

            words = section.split()

            start = 0

            while start < len(words):

                end = start + chunk_size

                chunk = " ".join(
                    words[start:end]
                )

                chunks.append(chunk)

                start += (
                    chunk_size
                    - overlap
                )

            continue

        # -------------------------------------------------
        # Merge sections intelligently
        # -------------------------------------------------

        combined_words = (

            current_chunk
            + " "
            + section
        ).split()

        if len(combined_words) <= chunk_size:

            current_chunk += (
                " " + section
            )

        else:

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = section

    # Final chunk
    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    return chunks


# ---------------------------------------------------------
# Main Chunking Function
# ---------------------------------------------------------

def chunk_text(text):

    sections = split_legal_sections(
        text
    )

    chunks = build_chunks(
        sections
    )

    return chunks