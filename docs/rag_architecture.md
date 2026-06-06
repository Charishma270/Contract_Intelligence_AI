# RAG Architecture

## Overview

The Contract Intelligence AI platform uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant legal clauses from contracts and generate explainable contract analysis results.

The architecture combines semantic search, keyword search, legal clause classification, risk assessment, and explainability modules.

---

## System Architecture

```text
User Query
    │
    ▼
Query Expansion
    │
    ▼
Embedding Generation
    │
    ▼
Hybrid Retrieval
 ┌─────────────┬─────────────┐
 │             │             │
 ▼             ▼
FAISS      BM25 Search
Semantic   Keyword
Search     Search
 │             │
 └──────┬──────┘
        ▼
Hybrid Fusion
        │
        ▼
Result Re-ranking
        │
        ▼
Retrieved Contract Clause
        │
        ▼
Legal-BERT Classification
        │
        ▼
Multi-Label Classification
        │
        ▼
Risk Scoring Engine
        │
        ▼
Explainability Generation
        │
        ▼
Contract Summary
        │
        ▼
Final Response
```

---

## Components

### Query Expansion

Enhances user queries using related legal terminology to improve retrieval recall.

Example:

* Termination → cancellation, exit, termination clause
* Liability → damages, indemnity, liability cap

---

### Embedding Generation

Contract clauses are converted into dense vector representations using the Sentence Transformers embedding model.

Model:

```text
all-MiniLM-L6-v2
```

---

### FAISS Semantic Search

Uses vector similarity search to retrieve semantically relevant clauses even when exact keywords are not present.

---

### BM25 Keyword Search

Performs traditional keyword-based retrieval for exact legal terminology matching.

---

### Hybrid Fusion

Combines FAISS semantic retrieval and BM25 keyword retrieval scores to improve overall retrieval quality.

---

### Result Re-ranking

Retrieved clauses are re-ranked using fusion scores to prioritize the most relevant contract sections.

---

### Legal-BERT Classification

Classifies retrieved clauses into legal categories such as:

* Termination
* Liability
* Confidentiality
* Intellectual Property
* Payment Terms
* Renewal

---

### Multi-Label Classification

Allows a clause to belong to multiple legal categories when appropriate.

---

### Risk Scoring

Evaluates the legal and business risk associated with each clause.

Outputs include:

* Risk Score
* Risk Level
* Risk Explanation

---

### Explainability Generation

Provides reasoning for predictions and highlights the factors contributing to the assigned risk score.

---

### Contract Summary

Generates an overall summary of the contract including:

* High-risk clauses
* Key obligations
* Critical legal concerns
* Overall contract risk

---

## Technologies Used

* Python
* FastAPI
* Sentence Transformers
* FAISS
* BM25
* Legal-BERT
* Scikit-Learn
* LangChain
* Docker

---

## Benefits

* Hybrid retrieval improves accuracy.
* Semantic search handles paraphrased legal language.
* Explainable AI improves trust and transparency.
* Risk scoring assists contract review.
* Scalable architecture supports large contract collections.

```
```
