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

                # -----------------------------------------
                # Safe overlap handling
                # -----------------------------------------

                step = max(
                    1,
                    chunk_size - overlap
                )

                start += step

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

            if current_chunk.strip():

                chunks.append(
                    current_chunk.strip()
                )

            current_chunk = section

    # -----------------------------------------------------
    # Final chunk
    # -----------------------------------------------------

    if current_chunk.strip():

        chunks.append(
            current_chunk.strip()
        )

    return chunks


# ---------------------------------------------------------
# Main Chunking Function
# ---------------------------------------------------------

def chunk_text(

    text,

    chunk_size=350,

    overlap=75
):

    # -----------------------------------------------------
    # Backward compatibility
    # -----------------------------------------------------

    if not text:

        return []

    sections = split_legal_sections(
        text
    )

    # -----------------------------------------------------
    # Fallback for non-legal/simple text
    # -----------------------------------------------------

    if len(sections) == 0:

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(
                words[start:end]
            )

            chunks.append(chunk)

            # ---------------------------------------------
            # Safe overlap handling
            # ---------------------------------------------

            step = max(
                1,
                chunk_size - overlap
            )

            start += step

        return chunks

    # -----------------------------------------------------
    # Legal-aware chunking
    # -----------------------------------------------------

    chunks = build_chunks(

        sections,

        chunk_size=chunk_size,

        overlap=overlap
    )

    return chunks