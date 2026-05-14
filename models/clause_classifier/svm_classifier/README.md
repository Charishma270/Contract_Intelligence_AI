# 🤖 LinearSVC Model Documentation

---

# 📂 Folder Structure

```txt
models/
└── svm_classifier/
    ├── svm_model.pkl
    ├── tfidf_vectorizer.pkl
    ├── metrics.json
    └── label_mapping.json
```

---

# 🎯 Purpose

This folder contains trained machine learning artifacts and evaluation outputs for the LinearSVC legal clause classification baseline.

The LinearSVC model was developed as a stronger classical NLP baseline after Logistic Regression demonstrated stable performance on clause-level legal text classification.

The goal of this model is to improve:
- recall
- F1-score
- clause detection reliability

before moving to transformer-based Legal-BERT fine-tuning.

---

# 📦 Stored Artifacts

---

# 1️⃣ `svm_model.pkl`

## Description
Serialized LinearSVC classifier trained on clause-level legal text snippets.

## Purpose
Predict whether a target legal clause is:
- present (`1`)
- absent (`0`)

for the selected legal clause categories.

## Training Pipeline

```txt
Clause Snippet
    ↓
TF-IDF Vectorization
    ↓
LinearSVC
    ↓
Binary Classification
```

---

# 2️⃣ `tfidf_vectorizer.pkl`

## Description
Serialized TF-IDF vectorizer fitted on the processed legal clause dataset.

## Purpose
Convert legal text into sparse numerical vectors suitable for classical NLP classifiers.

## Configuration

| Parameter | Value |
|---|---|
| Max Features | 10,000 |
| N-Gram Range | (1, 2) |
| Stop Words | English |
| Min DF | 2 |
| Max DF | 0.95 |

---

# 3️⃣ `metrics.json`

## Description
Stores evaluation metrics and model performance results for the LinearSVC classifier.

## Includes

- accuracy
- precision
- recall
- F1-score
- confusion matrix
- per-label performance
- TF-IDF configuration
- dataset split information

---

# 4️⃣ `label_mapping.json`

## Description
Stores:
- target label names
- label mappings
- dataset distribution statistics

## Target Labels

- Cap On Liability
- Renewal Term
- Termination For Convenience
- Uncapped Liability

---

# 📊 LinearSVC Model Performance

| Metric | Score |
|---|---|
| Accuracy | 93.9% |
| Precision | 94.9% |
| Recall | 87.9% |
| F1-Score | 91.3% |

---

# 🧠 Key Observations

- LinearSVC outperformed Logistic Regression across all major metrics
- Significant improvement observed in recall:
  - 81.9% → 87.9%
- False negatives reduced from:
  - 27 → 18
- Clause-level preprocessing dramatically improved classifier effectiveness
- Sparse TF-IDF vectors worked effectively with margin-based classification

---

# 🚧 Planned Future Models

Future versions of this folder may include:

- Legal-BERT fine-tuned models
- Transformer tokenizers
- Sentence embedding models
- Clause risk scoring models
- NER models
- Semantic retrieval models

---

# ⚠️ Important Notes

- `.pkl` files contain serialized Python objects
- The TF-IDF vectorizer must always be loaded together with the classifier
- Metrics and mappings should remain version-aligned with the trained model
- Current models are baseline research/development artifacts
- Not intended for production legal decision-making