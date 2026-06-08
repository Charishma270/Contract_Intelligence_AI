# Week 4 Progress Report

## Project

AI-Powered Contract Intelligence & Risk Scoring (NLP)

## Role

Frontend Engineer | DevOps Engineer | Deployment Engineer

## Objectives

* Complete advanced frontend modules.
* Integrate frontend with backend APIs.
* Improve chatbot user experience.
* Test Docker-based deployment.
* Verify application functionality.

---

## Work Completed

### Dashboard Enhancements

Implemented advanced dashboard components:

* Contracts Table
* Risk Distribution Chart
* Contract Details Section
* Quick Actions Panel
* Enhanced Recent Activity Tracking

The dashboard now provides a comprehensive overview of contract analysis activities and risk statistics.

---

### Analyze Page Integration

Successfully integrated frontend with backend contract analysis APIs.

Implemented display of:

* Fusion Score
* BM25 Score
* Rerank Score
* Confidence Score
* Risk Score
* AI Explanation
* Legal-BERT Prediction
* Classical Model Prediction
* Clause Text Viewer

Added:

* Risk badges
* Confidence visualization
* Read More / Show Less functionality
* Model disagreement warnings

---

### Chatbot Enhancements

Upgraded chatbot interface with advanced features:

#### Contract Selection

* Dynamic contract dropdown
* Contract-aware question answering

#### User Experience Improvements

* Auto-scroll support
* Loading indicators
* Suggested prompts
* Responsive message layout

#### Advanced Features

* Markdown rendering
* Copy response functionality
* Timestamps
* Typing animation
* Dark Mode support

---

### Backend Integration Testing

Verified integration with:

* Contract Upload API
* Contract Retrieval API
* Analysis API
* Chat API

Tested:

* Request handling
* Error handling
* Data rendering
* API response processing

---

## DevOps Activities

### Docker Installation

Successfully configured:

* Docker Desktop
* WSL2
* Docker Engine

Verified proper installation and environment setup.

---

### Docker Build Testing

Executed:

```bash
docker compose build --no-cache
```

Successfully built:

* Backend Container
* Worker Container

---

### Docker Compose Testing

Executed:

```bash
docker compose up
```

Verified:

* Redis container startup
* Celery worker startup
* Backend initialization process

---

### Deployment Debugging

Identified deployment issues:

#### Chat API Issues

* CORS configuration issue
* Backend response validation issue

#### Docker Deployment Issue

Detected missing machine learning model file:

```text
models/clause_classifier/svm_classifier/svm_model.pkl
```

Collaborated with backend team to verify deployment configuration and startup behavior.

---

## Technologies Used

### Frontend

* React
* Vite
* Tailwind CSS
* Axios
* React Router

### Backend Integration

* FastAPI
* Swagger

### DevOps

* Docker
* Docker Compose
* WSL2

---

## Challenges Faced

### Frontend Challenges

* Chatbot response formatting
* API integration debugging
* State management during asynchronous requests

### Deployment Challenges

* Docker environment setup
* Container startup debugging
* Missing model dependency identification
* API communication issues

---

## Key Learnings

* React application architecture
* Frontend-backend integration
* REST API communication
* Docker containerization
* Docker Compose orchestration
* Debugging deployment environments
* Team collaboration in a multi-role project

---

## Outcome

Successfully completed all assigned Frontend and DevOps responsibilities.

Completed modules:

* Dashboard
* Upload Contract Page
* Clause Viewer
* Analyze Page
* Chatbot Interface
* API Integration
* Docker Testing
* Deployment Verification

The application is capable of:

* Uploading contracts
* Analyzing clauses
* Displaying risk insights
* Retrieving semantic search results
* Supporting contract-aware chatbot interactions

Project status at the end of Week 4:

✅ Frontend Development Completed

✅ DevOps Responsibilities Completed

✅ Local Deployment Verification Completed
