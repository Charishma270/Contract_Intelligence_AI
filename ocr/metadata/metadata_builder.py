def create_metadata(contract_id, page_num, chunk_id, text, source_file):
    return {
        "contract_id": contract_id,
        "page": page_num,
        "chunk_id": chunk_id,
        "text": text,
        "source": source_file
    }