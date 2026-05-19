from rag.pipeline.pipeline import run_pipeline


def analyze_contract_query(query: str):

    results = run_pipeline(query)

    return results