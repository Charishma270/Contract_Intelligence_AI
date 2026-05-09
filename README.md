# Contract Intelligence AI

An AI-powered legal contract analysis platform designed to assist legal and compliance teams by automating contract understanding, clause detection, semantic search, and risk analysis.

---

# 🚀 Features

- Upload and analyze legal contract PDFs
- OCR-based text extraction from scanned contracts
- Named Entity Recognition (NER)
- Legal clause classification using Transformer models
- Contract risk analysis and scoring
- Semantic search using vector embeddings
- Conversational contract Q&A using RAG
- FastAPI backend integration
- React-based frontend interface
- Docker-ready deployment architecture

---

# 🧠 System Workflow

## Step 1 — Contract Upload
User uploads a legal contract PDF through the frontend interface.

## Step 2 — OCR Processing
OCR pipeline extracts readable text from the uploaded PDF.

## Step 3 — Text Preprocessing
Extracted text is cleaned, normalized, and split into meaningful chunks.

## Step 4 — Named Entity Recognition (NER)
NER model extracts:
- Organizations
- Dates
- Monetary values
- Jurisdictions
- Contract parties

## Step 5 — Clause Classification
Transformer-based NLP models identify legal clauses such as:
- Termination clauses
- Confidentiality clauses
- Liability clauses
- Auto-renewal clauses

## Step 6 — Risk Analysis
Risk engine evaluates extracted clauses and calculates contract risk scores using:
- Clause detection
- Rule-based heuristics
- Business logic analysis

## Step 7 — Embedding Generation
Sentence embeddings are generated for semantic understanding.

## Step 8 — Vector Database Storage
Embeddings are stored in a vector database to enable semantic retrieval.

## Step 9 — Conversational AI (RAG)
Users can ask natural language questions about the uploaded contract.

The system:
1. Retrieves relevant chunks using semantic search
2. Sends retrieved context to the LLM
3. Generates grounded responses

---

# 🛠️ Tech Stack

## Programming Language
- Python

## Backend
- FastAPI
- Uvicorn

## OCR
- Tesseract OCR
- pdf2image

## NLP / AI
- spaCy
- Hugging Face Transformers
- Legal-BERT / RoBERTa
- Sentence Transformers
- PyTorch

## Vector Search / RAG
- FAISS
- LangChain

## Conversational AI
- Llama 3 / Mistral

## Frontend
- React

## Deployment
- Docker
- AWS EC2

## Version Control
- Git
- GitHub

---

# 📂 Project Structure

```plaintext
CONTRACT_INTELLIGENCE_AI/
│
├── backend/
│   ├── api/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── data/
│   ├── embeddings/
│   ├── processed/
│   ├── raw/
│   └── sample_contracts/
│
├── docs/
│   ├── api_docs/
│   ├── architecture/
│   └── workflows/
│
├── frontend/
│   ├── components/
│   ├── public/
│   └── src/
│
├── logs/
│
├── models/
│   ├── clause_classifier/
│   ├── embeddings/
│   ├── llm/
│   └── ner/
│
├── notebooks/
│
├── ocr/
│   ├── extraction/
│   ├── outputs/
│   └── preprocessing/
│
├── rag/
│   ├── chunking/
│   ├── prompts/
│   ├── retrieval/
│   └── vector_db/
│
├── risk_engine/
│   ├── analysis/
│   ├── rules/
│   └── scoring/
│
├── scripts/
│
├── tests/
│   ├── backend/
│   ├── models/
│   └── rag/
│
├── uploads/
│
├── .gitignore
├── main.py
├── README.md
└── requirements.txt