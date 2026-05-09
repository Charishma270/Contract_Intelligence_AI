# ⚖️ Contract Intelligence AI

An AI-powered legal contract analysis platform designed to automate contract understanding, semantic retrieval, clause detection, and explainable risk analysis for legal and compliance teams.

This system combines OCR, NLP, Transformer-based clause classification, semantic vector search, Retrieval-Augmented Generation (RAG), and conversational AI into a unified enterprise-grade workflow.

---

# 🚀 Core Features

## 📄 Intelligent Contract Processing
- Upload legal contracts in PDF format
- OCR-based text extraction from scanned documents
- Automatic preprocessing and chunking of legal text

---

## 🧠 NLP & Contract Understanding
- Named Entity Recognition (NER)
- Legal clause classification using Transformer models
- Identification of:
  - Termination clauses
  - Liability clauses
  - Confidentiality clauses
  - Auto-renewal clauses
  - Payment obligations
  - Jurisdiction details

---

## ⚠️ Explainable Risk Analysis
- Rule-based legal risk scoring
- Detection of potentially dangerous clauses
- Business logic-driven contract evaluation
- Structured JSON-based analysis output

---

## 🔍 Semantic Search & Retrieval
- Embedding-based semantic search
- Context-aware retrieval using vector similarity
- Meaning-based contract exploration
- Retrieval-Augmented Generation (RAG)

---

## 🤖 Conversational Contract AI
- Ask natural language questions about uploaded contracts
- Grounded responses using retrieved contract context
- LLM-powered legal assistance workflow

---

## 🌐 Backend & Deployment
- REST API architecture using FastAPI
- Docker-ready deployment structure
- AWS-compatible infrastructure

---

# 🧠 System Workflow

## Step 1 — Contract Upload
The user uploads a legal contract through the frontend interface.

↓

## Step 2 — OCR Processing
OCR extracts readable text from scanned PDFs and image-based contracts.

↓

## Step 3 — Text Preprocessing
The extracted text is:
- cleaned
- normalized
- segmented into semantic chunks

↓

## Step 4 — Named Entity Recognition (NER)
NER models identify and extract:
- Organizations
- Contract parties
- Dates
- Monetary values
- Jurisdictions
- Legal references

↓

## Step 5 — Clause Classification
Transformer-based models classify legal clauses into predefined categories.

Examples:
- Termination
- Liability
- Confidentiality
- Auto-renewal
- Indemnification

↓

## Step 6 — Risk Analysis Engine
Business rules and heuristics evaluate contract risks.

Example:
- unlimited liability
- missing liability cap
- auto-renewal risks
- vague termination conditions

↓

## Step 7 — Embedding Generation
Sentence embeddings are generated from contract chunks.

These embeddings capture semantic meaning rather than exact keywords.

↓

## Step 8 — Vector Database Storage
Embeddings are stored inside a vector database for semantic retrieval.

↓

## Step 9 — Conversational AI (RAG)
Users ask questions about the contract.

The system:
1. retrieves relevant chunks using semantic similarity
2. injects retrieved context into prompts
3. generates grounded responses using an LLM

---

# 🛠️ Technology Stack

## Programming Language
- Python

---

## Backend Framework
- FastAPI
- Uvicorn

---

## OCR Pipeline
- Tesseract OCR
- pdf2image

---

## NLP & Deep Learning
- spaCy
- Hugging Face Transformers
- Legal-BERT
- RoBERTa
- Sentence Transformers
- PyTorch

---

## Semantic Retrieval / RAG
- FAISS
- LangChain

---

## Conversational LLM
- Llama 3
- Mistral

---

## Frontend
- React

---

## Deployment & Infrastructure
- Docker
- AWS EC2

---

## Version Control
- Git
- GitHub

---

# 📂 Project Architecture

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

# 👥 Team Responsibilities

| Team Member | Responsibility |
|---|---|
| Member 1 | OCR & Document Processing |
| Member 2 | NLP / NER / Clause Classification |
| Member 3 | Embeddings / RAG / Vector Database |
| Member 4 | Backend API Development |
| Member 5 | Frontend / Deployment / DevOps |

---

# ⚙️ Local Setup

## 1. Clone Repository

```bash
git clone <repository-url>

## 2. Navigate to Project Directory

```bash
cd CONTRACT_INTELLIGENCE_AI

## 3. Create Virtual Environment

```bash
python -m venv contract_ai_env

## 4. Activate Virtual Environment
Windows

```bash
contract_ai_env\Scripts\activate

Linux / macOS

```bash
source contract_ai_env/bin/activate

## 5. Install Dependencies

```bash
pip install -r requirements.txt

## 6. Run Backend Server

```bash
uvicorn main:app --reload

# 📌 Current Development Status

## ✅ Completed

- Project architecture planning
- Folder structure setup
- Environment setup
- Dependency management
- Git & GitHub initialization
- Workflow design

---

## 🚧 In Progress

- OCR pipeline development
- Text preprocessing pipeline
- FastAPI backend initialization

---

## ⏳ Planned

- NER integration
- Clause classification model
- Vector search implementation
- RAG conversational pipeline
- Frontend dashboard
- Docker deployment
- AWS deployment

---

# 🎯 Project Objective

To build an enterprise-grade AI-powered contract intelligence system capable of:

- automated legal document understanding
- semantic contract retrieval
- explainable risk analysis
- conversational contract exploration using modern NLP and LLM architectures

---

# ⚠️ Disclaimer

This project is intended for educational and research purposes.

Generated outputs should not be considered professional legal advice.