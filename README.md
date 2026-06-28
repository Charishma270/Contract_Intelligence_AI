# ⚖️ Contract Intelligence AI

<p align="center">
AI-Powered Legal Contract Analysis, Semantic Retrieval, Risk Assessment & Conversational Intelligence
</p>

---

# 📌 Overview

**Contract Intelligence AI** is an enterprise-inspired AI platform developed to simplify legal contract review by combining modern Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), semantic search, explainable AI, and intelligent document processing.

The platform enables users to upload legal contracts, automatically extract and preprocess text, classify legal clauses, perform explainable risk analysis, retrieve relevant contractual information using hybrid search, and interact with contracts through a conversational AI assistant.

Designed with a modular architecture, the project integrates OCR, transformer-based models, vector databases, backend APIs, authentication, and a responsive web interface into a single intelligent contract analysis system.

---

# 🚀 Key Features

## 📄 Intelligent Contract Processing

* Upload legal contracts in PDF format
* OCR support for scanned contracts
* Automatic text extraction
* Document preprocessing and normalization
* Intelligent legal text chunking

---

## 🧠 Legal Clause Classification

Transformer-based legal clause identification using Legal NLP models.

Supported clause categories include:

* Confidentiality
* Termination
* Liability
* Payment
* Jurisdiction
* Indemnification
* Auto-Renewal
* Force Majeure
* Governing Law
* Intellectual Property
* Warranty
* Dispute Resolution

---

## ⚠️ Explainable Risk Analysis

The platform evaluates contracts using predefined legal business rules and AI-assisted analysis.

Features include:

* Risk scoring
* Risk severity classification
* Clause-wise explanations
* Missing clause detection
* High-risk obligation identification
* Explainable JSON output

---

## 🔍 Hybrid Semantic Retrieval

Hybrid retrieval combines dense and sparse search techniques for improved legal document retrieval.

Implemented using:

* FAISS Vector Search
* BM25 Ranking
* Sentence Transformers
* Metadata-aware Retrieval
* Query Expansion
* Hybrid Score Fusion
* Retrieval Re-ranking

---

## 🤖 Conversational AI

Ask natural language questions about uploaded contracts.

Examples:

* What are the termination conditions?
* Is there unlimited liability?
* Who are the contracting parties?
* What are the payment obligations?
* Does this contract auto-renew?

Responses are generated using Retrieval-Augmented Generation (RAG) grounded in retrieved contract content.

---

## 🔐 Authentication & Security

Secure user authentication system including:

* User Registration
* Login & Logout
* JWT Authentication
* Time-based One-Time Password (TOTP) Two-Factor Authentication
* Password Reset Workflow
* Protected API Endpoints
* Secure Password Hashing

---

## 📊 Analytics & Explainability

* Clause classification confidence
* Retrieval analytics
* Explainable AI outputs
* Structured JSON responses
* Risk summaries

---

## 🌐 REST API

Backend APIs provide:

* Authentication
* Contract Upload
* OCR Processing
* Clause Analysis
* Risk Assessment
* Semantic Retrieval
* Chat Assistant
* User Profile Management

---

# 🏗️ System Workflow

```
User Uploads Contract
          │
          ▼
OCR Text Extraction
          │
          ▼
Text Cleaning & Preprocessing
          │
          ▼
Legal Text Chunking
          │
          ▼
Named Entity Recognition
          │
          ▼
Legal Clause Classification
          │
          ▼
Risk Analysis Engine
          │
          ▼
Embedding Generation
          │
          ▼
FAISS + BM25 Hybrid Retrieval
          │
          ▼
Conversational AI (RAG)
          │
          ▼
Explainable Results
```

---

# 🧠 AI Pipeline

The platform follows a complete legal document intelligence pipeline:

1. Contract Upload
2. OCR Text Extraction
3. Text Preprocessing
4. Legal Chunk Generation
5. Named Entity Recognition
6. Legal Clause Classification
7. Explainable Risk Analysis
8. Embedding Generation
9. Hybrid Retrieval (FAISS + BM25)
10. Retrieval Re-ranking
11. Conversational Question Answering
12. Explainable AI Response Generation

---

# 🛠️ Technology Stack

## Programming Language

* Python

---

## Backend

* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy

---

## Frontend

* React
* Vite
* JavaScript
* HTML5
* CSS3

---

## Authentication

* JWT Authentication
* Passlib
* PyJWT
* TOTP Two-Factor Authentication

---

## OCR

* Tesseract OCR
* pdf2image
* pdfplumber

---

## Machine Learning & NLP

* Hugging Face Transformers
* Sentence Transformers
* spaCy
* Legal-BERT
* PyTorch
* Scikit-learn

---

## Retrieval-Augmented Generation

* FAISS
* BM25
* LangChain

---

## Data Processing

* Pandas
* NumPy
* SciPy

---

## Background Processing

* Celery
* Redis

---

## Deployment

* Docker
* Docker Compose

> AWS deployment is planned as the production deployment target after project submission.

---

## Version Control

* Git
* GitHub

---

# 📂 Project Structure

```text
CONTRACT_INTELLIGENCE_AI/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── middleware/
│   └── database/
│
├── frontend/
│
├── rag/
│   ├── chunking/
│   ├── retrieval/
│   ├── prompts/
│   ├── pipeline/
│   └── vector_store/
│
├── risk_engine/
│
├── data/
│
├── uploads/
│
├── tests/
│
├── docs/
│
├── logs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── main.py
```

---

# 👥 Team Contributions

| Team Member             | Role                               | Major Contributions                                                                                                                                    |
| ----------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Sruthi Lakshmi Mada** | OCR & Document Processing Engineer | OCR pipeline, PDF preprocessing, document extraction, preprocessing workflow, data preparation                                                         |
| **Charishma Ganta**     | Legal AI Engineer                  | Legal clause classification, transformer integration, risk analysis modules, Legal-BERT integration                                                    |
| **Tisha Soni**          | AI Retrieval & LLM Engineer        | Hybrid Retrieval (FAISS + BM25), RAG pipeline, semantic search, retrieval analytics, metadata-aware indexing, reranking, conversational AI integration |
| **Shah Rushabh**        | Backend & System Integration Lead  | FastAPI backend, REST APIs, JWT authentication, TOTP 2FA, backend integration, database management, testing                                            |
| **Mukt Patel**          | Frontend, DevOps & QA Engineer     | React frontend, authentication UI, dashboard, notifications, Docker configuration, deployment setup, testing                                           |

---

# ⚙️ Local Setup

## Clone Repository

```bash
git clone <repository-url>
```

## Navigate to Project

```bash
cd Contract_Intelligence_AI
```

## Create Virtual Environment

```bash
python -m venv contract_ai_env
```

## Activate Environment

Windows

```bash
contract_ai_env\Scripts\activate
```

Linux / macOS

```bash
source contract_ai_env/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn main:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 🐳 Docker

Build the application:

```bash
docker compose build
```

Run all services:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

---

# 🧪 Testing

The project includes testing for:

* Backend APIs
* Authentication
* Clause Classification
* Retrieval Pipeline
* Risk Analysis
* Performance
* End-to-End Workflow

Run tests using:

```bash
pytest
```

---

# 🎯 Project Objectives

The primary objective of this project is to build an intelligent legal contract analysis platform capable of:

* Understanding legal documents automatically
* Identifying important legal clauses
* Explaining contractual risks
* Enabling semantic contract retrieval
* Supporting conversational legal document exploration
* Improving legal review efficiency using Artificial Intelligence

---

# 🚀 Future Enhancements

* AWS Cloud Deployment
* CI/CD Pipeline
* Multi-language Contract Support
* Contract Comparison Engine
* Clause Recommendation System
* User Collaboration Features
* Advanced Legal Analytics Dashboard
* Model Fine-Tuning on Custom Legal Datasets

---

# 📜 License

This project has been developed for academic, educational, and research purposes.

---

# ⚠️ Disclaimer

This application is designed as an AI-assisted legal document analysis system for educational and research use. It is **not** a substitute for professional legal advice. Users should consult qualified legal professionals before making legal or contractual decisions based on the generated analysis.
