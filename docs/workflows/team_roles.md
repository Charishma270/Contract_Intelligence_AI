# 👥 TEAM ROLES & RESPONSIBILITIES

---

# 🚀 AI-Powered Contract Intelligence & Risk Scoring System

## Using
- CUAD Dataset
- Legal NLP
- RAG Architecture
- LLM-based Contract Understanding

## Dataset
https://huggingface.co/datasets/theatticusproject/cuad

---

# 🎯 PROJECT GOAL

Build an AI system that can:

- Read uploaded contracts
- Extract legal entities
- Detect important clauses
- Analyze risks
- Perform semantic search
- Answer contract-related questions using LLMs

---

# 🧠 IMPORTANT PROJECT REALITY

This project is **NOT** just:

```txt
train model → done
```

This is a:

- Software engineering project
- AI engineering project
- Systems integration project
- Deployment project
- Collaboration project

The hardest part will usually be:

```txt
 Integration
```

NOT model training.

---

# 🏗️ FINAL SYSTEM ARCHITECTURE FLOW

```txt
Frontend Upload
        ↓
FastAPI Backend
        ↓
OCR & Document Processing
        ↓
Text Cleaning
        ↓
Chunking + Metadata
        ↓
NER + Clause Classification
        ↓
Risk Scoring
        ↓
Embedding Generation
        ↓
FAISS Vector Database
        ↓
RAG Retrieval
        ↓
LLM Response Generation
        ↓
Frontend Dashboard + Chatbot
```

---

# 📂 FINAL COMMON PROJECT STRUCTURE

## EVERYONE MUST FOLLOW THIS STRUCTURE

```txt
project-root/
│
├── backend/
│   ├── api/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── config/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── hooks/
│       └── utils/
│
├── ocr/
│   ├── extraction/
│   ├── preprocessing/
│   └── outputs/
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
├── models/
│   ├── clause_classifier/
│   ├── embeddings/
│   ├── llm/
│   └── ner/
│
├── schemas/
│   ├── common/
│   ├── api/
│   └── models/
│
├── shared/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── uploads/
├── logs/
├── notebooks/
├── tests/
├── docs/
├── scripts/
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md
└── main.py
```

---

# 👤 MEMBER 1 — OCR, DOCUMENT PROCESSING & DATA ENGINEER

## 🎯 Main Responsibility

Convert uploaded contracts into clean, structured, AI-ready text.

---

## 🧠 Concepts to Understand

- OCR
- PDF parsing
- Image preprocessing
- Text cleaning
- Chunking
- Metadata handling
- CUAD preprocessing

---

## ⚙️ Responsibilities

### 📄 PDF Handling

Handle:

- Uploaded PDFs
- Scanned contracts
- Image-based contracts
- Multi-page documents

---

### 🔍 OCR Pipeline

#### Using
- Tesseract OCR
- pdf2image

#### Tasks
- Page extraction
- OCR text extraction
- Scanned document handling

---

### 🧹 Text Cleaning

Clean:

- Broken text
- Spacing errors
- OCR noise
- Artifacts

---

### ✂️ Chunking Strategy

VERY IMPORTANT.

Create:

- Semantic chunks
- Overlapping chunks
- Token-safe chunks

#### Suggested

```python
chunk_size = 500
chunk_overlap = 100
```

---

### 🧠 Metadata Generation

Every chunk MUST contain:

```json
{
  "contract_id": "",
  "chunk_id": "",
  "page_number": 1,
  "chunk_text": ""
}
```

This helps:

- Frontend highlighting
- Chatbot citations
- Debugging

---

### 📦 CUAD Dataset Preparation

#### Tasks
- Inspect CUAD structure
- Parse annotations
- Create train/test splits
- Preprocess labels

---

## 🛠️ Technologies

- Python
- Tesseract
- pdf2image
- regex
- nltk/spacy preprocessing

---

## 📌 Deliverables

- ✅ OCR pipeline
- ✅ Clean text extraction
- ✅ Chunked contracts
- ✅ Metadata-enriched chunks
- ✅ Processed CUAD dataset

---

# 👤 MEMBER 2 — LEGAL AI ENGINEER (NLP + CLAUSE ANALYSIS)

## 🎯 Main Responsibility

Build AI models that understand legal contracts.

---

## 🧠 Concepts to Understand

- transformers
- tokenization
- embeddings
- legal NLP
- clause classification
- fine-tuning
- inference

---

## ⚙️ Responsibilities

### 🧠 Named Entity Recognition (NER)

Extract:

- Organizations
- Dates
- Money values
- Jurisdictions
- Contract parties

#### Using
- spaCy
- transformers

---

### ⚖️ Clause Classification

Initially focus ONLY on:

- Termination
- Confidentiality
- Liability
- Auto Renewal

DO NOT start with all 41 CUAD labels initially.

---

### 🤖 Transformer Fine-Tuning

#### Use
- Legal-BERT
- RoBERTa

#### Tasks
- Tokenization
- Label mapping
- Training
- Evaluation
- Inference

---

### 📊 Evaluation

#### Metrics
- Precision
- Recall
- F1-score

---

### 🚨 Risk Scoring Logic

#### Example

- Unlimited liability → High Risk
- Auto renewal → Medium Risk
- Missing termination clause → High Risk

---

### 📦 Structured Output Format

```json
{
  "clause_type": "",
  "risk_level": "",
  "confidence": 0.0,
  "page_number": 1
}
```

---

## 🛠️ Technologies

- Hugging Face Transformers
- PyTorch
- spaCy
- tokenizers

---

## 📌 Deliverables

- ✅ Clause classifier
- ✅ NER pipeline
- ✅ Risk scoring logic
- ✅ Structured AI outputs
- ✅ Inference pipeline

---

# 👤 MEMBER 3 — AI RETRIEVAL & LLM ENGINEER (RAG)

## 🎯 Main Responsibility

Build semantic search and conversational AI.

---

## 🧠 Concepts to Understand

- embeddings
- semantic similarity
- vector databases
- RAG
- prompt engineering
- LLM orchestration

---

## ⚙️ Responsibilities

### 🧬 Embedding Generation

#### Using
- Sentence Transformers

#### Recommended Model

```python
all-MiniLM-L6-v2
```

Generate embeddings for:

- Chunks
- User queries

---

### 🗂️ Vector Database

Initially use:

```txt
FAISS
```

NOT Pinecone initially.

Keep setup simple first.

---

### 🔍 Semantic Retrieval

Retrieve semantically similar chunks.

#### Example

```txt
"What are the termination risks?"
```

---

### 🔗 LangChain Integration

Build:

- Retrievers
- Chains
- Prompt workflows
- Context injection

---

### 🤖 RAG Pipeline

```txt
User Query
    ↓
Embedding Search
    ↓
Retrieve Relevant Chunks
    ↓
Inject Context into Prompt
    ↓
LLM Generates Response
```

---

### 💬 Contract Chatbot

Develop:

- Contract Q&A
- AI summaries
- Risk explanations

---

### 🚨 Hallucination Reduction

Implement:

- Grounded responses
- Source-aware answering
- Citation-aware answers

#### Example

```txt
"According to Page 7..."
```

---

### 🔔 Embedding Version Tracking

Track:

- Embedding models
- Retrieval configurations
- Chunking configurations

#### Example

```python
embedding_model = "all-MiniLM-L6-v2"
top_k = 5
```

---

## 🛠️ Technologies

- Sentence Transformers
- FAISS
- LangChain
- Hugging Face
- Llama 3

---

## 📌 Deliverables

- ✅ Embedding pipeline
- ✅ FAISS vector DB
- ✅ RAG workflow
- ✅ Contract chatbot
- ✅ AI summaries & Q&A

---

# 👤 MEMBER 4 — BACKEND & SYSTEMS INTEGRATION LEAD

## 🎯 Main Responsibility

Connect ALL modules into ONE working system.

---

## 🧠 Concepts to Understand

- APIs
- async workflows
- JSON schemas
- backend orchestration
- integration

---

## ⚙️ Responsibilities

### 🌐 FastAPI Backend

Build:

- Backend architecture
- Routing
- Request handling

---

### 🔌 API Endpoints

```http
POST /upload
POST /analyze
POST /chat
GET  /contracts
GET  /risk-score
```

---

### 🔄 Pipeline Integration

Connect:

- OCR
- NLP
- RAG
- frontend

This role acts as the:

```txt
🔥 Technical Lead
```

---

### 🧠 Shared Schema Management

Maintain:

```txt
schemas/
shared_models/
```

---

### ⚡ Async Processing

Handle:

- Large contract processing
- Long inference jobs
- Background tasks

---

### 📦 Standardized API Responses

```json
{
  "contract_id": "",
  "risk_score": 0,
  "entities": [],
  "clauses": [],
  "summary": ""
}
```

---

### 🔒 Error Handling

Implement:

- Validation
- Exception handling
- API stability

---

### 🔀 Git Coordination

#### Responsibilities
- PR reviews
- Merge coordination
- API consistency
- Schema consistency

---

### 🔔 API Documentation Responsibility

Maintain:

```txt
Swagger/OpenAPI docs
docs/api_contracts.md
```

---

## 🛠️ Technologies

- FastAPI
- Uvicorn
- Pydantic
- async Python

---

## 📌 Deliverables

- ✅ Backend APIs
- ✅ Integrated workflows
- ✅ Shared schemas
- ✅ Stable orchestration
- ✅ Unified backend system

---

# 👤 MEMBER 5 — FRONTEND, DEVOPS & QA ENGINEER

## 🎯 Main Responsibility

Build UI and deploy the complete system.

---

## 🧠 Concepts to Understand

- React
- frontend architecture
- API integration
- Docker
- deployment
- testing

---

## ⚙️ Responsibilities

### 🎨 Frontend Dashboard

Build:

- Upload page
- Dashboard
- Clause viewer
- Chatbot UI
- Risk visualization

---

### 🔗 Frontend ↔ Backend Integration

Integrate frontend with backend APIs.

---

### 📊 Visualization

Display:

- Risk scores
- Highlighted clauses
- Extracted entities
- Summaries

---

### 🐳 Dockerization

Create:

- Dockerfiles
- docker-compose.yml

---

### ☁️ Deployment

Deploy on:

```txt
AWS EC2
```

---

### 🧪 QA & Testing

Test:

- Upload flow
- Chatbot flow
- Frontend rendering
- API integration

---

### 📈 Monitoring

Display:

- Loading states
- Inference progress
- Processing logs

---

## 🛠️ Technologies

- React
- TailwindCSS
- Axios
- Docker
- AWS

---

## 📌 Deliverables

- ✅ Frontend dashboard
- ✅ Chatbot UI
- ✅ Dockerized deployment
- ✅ Cloud deployment
- ✅ Testing workflows

---

# 🔥 COMMON RULES EVERYONE MUST FOLLOW

## 📦 COMMON VARIABLE NAMES

EVERYONE MUST USE SAME VARIABLE NAMES.

### ✅ USE THESE

```txt
contract_id
chunk_id
chunk_text
page_number
risk_score
entities
clauses
summary
embedding
user_query
retrieved_chunks
```

---

### ❌ NEVER RANDOMLY CHANGE VARIABLE NAMES

BAD:

```txt
docId
riskScore
chunkTxt
```

This causes integration failure.

---

# 📦 COMMON JSON STRUCTURES

## CONTRACT FORMAT

```json
{
  "contract_id": "",
  "filename": "",
  "upload_time": "",
  "chunks": [],
  "entities": [],
  "clauses": [],
  "risk_score": 0,
  "summary": ""
}
```

---

## CHUNK FORMAT

```json
{
  "chunk_id": "",
  "contract_id": "",
  "page_number": 1,
  "chunk_text": "",
  "embedding": []
}
```

---

## ENTITY FORMAT

```json
{
  "entity_type": "",
  "entity_value": "",
  "page_number": 1
}
```

---

## CLAUSE FORMAT

```json
{
  "clause_type": "",
  "risk_level": "",
  "confidence": 0.0,
  "page_number": 1
}
```

---

# 🔥 GIT WORKFLOW

## 🌿 Branch Structure

```txt
main
develop

feature/ocr
feature/nlp
feature/rag
feature/backend
feature/frontend
```

---

## ✅ DAILY GIT FLOW

Every member:

```bash
git checkout develop
git pull origin develop

git checkout feature/your-branch

# work
# commit
# push

# create PR → develop
```

---

## 🚫 NEVER

- ❌ Push directly to main
- ❌ Work on outdated code
- ❌ Merge without testing

---

## ✅ COMMIT MESSAGE FORMAT

```txt
week1-mon: implemented OCR extraction pipeline
week1-tue: added clause classification inference
week2-wed: integrated FAISS retrieval
```

---

# 🔥 WEEKLY INTEGRATION RULE

At the end of EVERY week:

ALL members MUST:

- Merge into develop
- Test complete pipeline
- Validate schemas
- Fix broken APIs
- Resolve merge conflicts

---

# 🔥 ORDER OF DEVELOPMENT

```txt
1. OCR Pipeline
        ↓
2. NLP Pipeline
        ↓
3. Embeddings + RAG
        ↓
4. Backend Integration
        ↓
5. Frontend Integration
        ↓
6. Deployment
```

---

# 🔥 ENVIRONMENT VARIABLES RULE

NEVER hardcode:

- API keys
- Tokens
- AWS credentials
- Model secrets

Use:

```txt
.env
```

---

# 🔥 IMPORTANT PROJECT REALITY

Your biggest challenge will NOT be:

- transformers
- LLMs
- embeddings

It will be:

```txt
integration consistency
```

That’s why:

- Shared schemas
- Shared variable names
- Git discipline
- Common APIs
- Structured workflow

matter MORE than fancy models.