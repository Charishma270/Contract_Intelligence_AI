👥 FINAL TEAM ROLES & RESPONSIBILITIES
🚀 AI-Powered Contract Intelligence & Risk Scoring System

Using:

CUAD Dataset
Legal NLP
RAG Architecture
LLM-based Contract Understanding

Dataset:
CUAD Dataset

🎯 PROJECT GOAL

Build an AI system that can:

Read uploaded contracts
Extract legal entities
Detect important clauses
Analyze risks
Perform semantic search
Answer contract-related questions using LLMs
🧠 IMPORTANT PROJECT REALITY

This project is NOT just:

train model → done

This is a:

software engineering project
AI engineering project
systems integration project
deployment project
collaboration project

The hardest part will usually be:

🔥 integration

NOT model training.

🏗️ FINAL SYSTEM ARCHITECTURE FLOW
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
📂 FINAL COMMON PROJECT STRUCTURE

EVERYONE MUST FOLLOW THIS STRUCTURE.

project-root/
│
├── backend/
├── frontend/
├── ocr/
├── nlp/
├── rag/
├── shared/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── uploads/
├── logs/
├── schemas/
├── docs/
├── tests/
│
├── .env
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
👤 MEMBER 1 — OCR, DOCUMENT PROCESSING & DATA ENGINEER
🎯 Main Responsibility

Convert uploaded contracts into clean, structured, AI-ready text.

🧠 Concepts to Understand
OCR
PDF parsing
image preprocessing
text cleaning
chunking
metadata handling
CUAD preprocessing
⚙️ Responsibilities
📄 PDF Handling

Handle:

uploaded PDFs
scanned contracts
image-based contracts
multi-page documents
🔍 OCR Pipeline

Using:

Tesseract OCR
pdf2image

Tasks:

page extraction
OCR text extraction
scanned document handling
🧹 Text Cleaning

Clean:

broken text
spacing errors
OCR noise
artifacts
✂️ Chunking Strategy

VERY IMPORTANT.

Create:

semantic chunks
overlapping chunks
token-safe chunks

Suggested:

chunk_size = 500
chunk_overlap = 100
🧠 Metadata Generation

Every chunk MUST contain:

{
  "contract_id": "",
  "chunk_id": "",
  "page_number": 1,
  "chunk_text": ""
}

This helps:

frontend highlighting
chatbot citations
debugging
📦 CUAD Dataset Preparation

Tasks:

inspect CUAD structure
parse annotations
create train/test splits
preprocess labels
🛠️ Technologies
Python
Tesseract
pdf2image
regex
nltk/spacy preprocessing
📌 Deliverables

✅ OCR pipeline
✅ Clean text extraction
✅ Chunked contracts
✅ Metadata-enriched chunks
✅ Processed CUAD dataset

👤 MEMBER 2 — LEGAL AI ENGINEER (NLP + CLAUSE ANALYSIS)
🎯 Main Responsibility

Build AI models that understand legal contracts.

🧠 Concepts to Understand
transformers
tokenization
embeddings
legal NLP
clause classification
fine-tuning
inference
⚙️ Responsibilities
🧠 Named Entity Recognition (NER)

Extract:

organizations
dates
money values
jurisdictions
contract parties

Using:

spaCy
transformers
⚖️ Clause Classification

Initially focus ONLY on:

Termination
Confidentiality
Liability
Auto Renewal

DO NOT start with all 41 CUAD labels initially.

🤖 Transformer Fine-Tuning

Use:

Legal-BERT
RoBERTa

Tasks:

tokenization
label mapping
training
evaluation
inference
📊 Evaluation

Metrics:

precision
recall
F1-score
🚨 Risk Scoring Logic

Example:

Unlimited liability → High Risk
Auto renewal → Medium Risk
Missing termination clause → High Risk
📦 Structured Output Format
{
  "clause_type": "",
  "risk_level": "",
  "confidence": 0.0,
  "page_number": 1
}
🛠️ Technologies
Hugging Face Transformers
PyTorch
spaCy
tokenizers
📌 Deliverables

✅ Clause classifier
✅ NER pipeline
✅ Risk scoring logic
✅ Structured AI outputs
✅ Inference pipeline

👤 MEMBER 3 — AI RETRIEVAL & LLM ENGINEER (RAG)
🎯 Main Responsibility

Build semantic search and conversational AI.

🧠 Concepts to Understand
embeddings
semantic similarity
vector databases
RAG
prompt engineering
LLM orchestration
⚙️ Responsibilities
🧬 Embedding Generation

Using:

Sentence Transformers

Recommended model:

all-MiniLM-L6-v2

Generate embeddings for:

chunks
user queries
🗂️ Vector Database

Initially use:

FAISS

NOT Pinecone initially.

Keep setup simple first.

🔍 Semantic Retrieval

Retrieve semantically similar chunks.

Example:

"What are the termination risks?"
🔗 LangChain Integration

Build:

retrievers
chains
prompt workflows
context injection
🤖 RAG Pipeline
User Query
    ↓
Embedding Search
    ↓
Retrieve Relevant Chunks
    ↓
Inject Context into Prompt
    ↓
LLM Generates Response
💬 Contract Chatbot

Develop:

contract Q&A
AI summaries
risk explanations
🚨 Hallucination Reduction

Implement:

grounded responses
source-aware answering
citation-aware answers

Example:

"According to Page 7..."
🔔 Embedding Version Tracking

Track:

embedding models
retrieval configurations
chunking configurations

Example:

embedding_model = "all-MiniLM-L6-v2"
top_k = 5
🛠️ Technologies
Sentence Transformers
FAISS
LangChain
Hugging Face
Llama 3
📌 Deliverables

✅ Embedding pipeline
✅ FAISS vector DB
✅ RAG workflow
✅ Contract chatbot
✅ AI summaries & Q&A

👤 MEMBER 4 — BACKEND & SYSTEMS INTEGRATION LEAD
🎯 Main Responsibility

Connect ALL modules into ONE working system.

🧠 Concepts to Understand
APIs
async workflows
JSON schemas
backend orchestration
integration
⚙️ Responsibilities
🌐 FastAPI Backend

Build:

backend architecture
routing
request handling
🔌 API Endpoints
POST /upload
POST /analyze
POST /chat
GET  /contracts
GET  /risk-score
🔄 Pipeline Integration

Connect:

OCR
NLP
RAG
frontend

This role acts as the:

🔥 Technical Lead
🧠 Shared Schema Management

Maintain:

schemas/
shared_models/
⚡ Async Processing

Handle:

large contract processing
long inference jobs
background tasks
📦 Standardized API Responses
{
  "contract_id": "",
  "risk_score": 0,
  "entities": [],
  "clauses": [],
  "summary": ""
}
🔒 Error Handling

Implement:

validation
exception handling
API stability
🔀 Git Coordination

Responsibilities:

PR reviews
merge coordination
API consistency
schema consistency
🔔 API Documentation Responsibility

Maintain:

Swagger/OpenAPI docs
docs/api_contracts.md
🛠️ Technologies
FastAPI
Uvicorn
Pydantic
async Python
📌 Deliverables

✅ Backend APIs
✅ Integrated workflows
✅ Shared schemas
✅ Stable orchestration
✅ Unified backend system

👤 MEMBER 5 — FRONTEND, DEVOPS & QA ENGINEER
🎯 Main Responsibility

Build UI and deploy the complete system.

🧠 Concepts to Understand
React
frontend architecture
API integration
Docker
deployment
testing
⚙️ Responsibilities
🎨 Frontend Dashboard

Build:

upload page
dashboard
clause viewer
chatbot UI
risk visualization
🔗 Frontend ↔ Backend Integration

Integrate frontend with backend APIs.

📊 Visualization

Display:

risk scores
highlighted clauses
extracted entities
summaries
🐳 Dockerization

Create:

Dockerfiles
docker-compose.yml
☁️ Deployment

Deploy on:

AWS EC2
🧪 QA & Testing

Test:

upload flow
chatbot flow
frontend rendering
API integration
📈 Monitoring

Display:

loading states
inference progress
processing logs
🛠️ Technologies
React
TailwindCSS
Axios
Docker
AWS
📌 Deliverables

✅ Frontend dashboard
✅ Chatbot UI
✅ Dockerized deployment
✅ Cloud deployment
✅ Testing workflows

🔥 COMMON RULES EVERYONE MUST FOLLOW
📦 COMMON VARIABLE NAMES

EVERYONE MUST USE SAME VARIABLE NAMES.

✅ USE THESE
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
❌ NEVER RANDOMLY CHANGE VARIABLE NAMES

BAD:

docId
riskScore
chunkTxt

This causes integration failure.

📦 COMMON JSON STRUCTURES
CONTRACT FORMAT
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
CHUNK FORMAT
{
  "chunk_id": "",
  "contract_id": "",
  "page_number": 1,
  "chunk_text": "",
  "embedding": []
}
ENTITY FORMAT
{
  "entity_type": "",
  "entity_value": "",
  "page_number": 1
}
CLAUSE FORMAT
{
  "clause_type": "",
  "risk_level": "",
  "confidence": 0.0,
  "page_number": 1
}
🔥 GIT WORKFLOW
🌿 Branch Structure
main
develop

feature/ocr
feature/nlp
feature/rag
feature/backend
feature/frontend
✅ DAILY GIT FLOW

Every member:

git checkout develop
git pull origin develop

git checkout feature/your-branch

work
commit
push

create PR → develop
🚫 NEVER

❌ Push directly to main
❌ Work on outdated code
❌ Merge without testing

✅ COMMIT MESSAGE FORMAT
week1-mon: implemented OCR extraction pipeline
week1-tue: added clause classification inference
week2-wed: integrated FAISS retrieval
🔥 WEEKLY INTEGRATION RULE

At end of EVERY week:

ALL members MUST:

merge into develop
test complete pipeline
validate schemas
fix broken APIs
resolve merge conflicts
🔥 ORDER OF DEVELOPMENT
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
🔥 ENVIRONMENT VARIABLES RULE

NEVER hardcode:

API keys
tokens
AWS credentials
model secrets

Use:

.env
🔥 IMPORTANT PROJECT REALITY

Your biggest challenge will NOT be:

transformers
LLMs
embeddings

It will be:

integration consistency

That’s why:

shared schemas
shared variable names
Git discipline
common APIs
structured workflow

matter MORE than fancy models.