# 🤖 Models Documentation

---

# 📂 Folder Structure

```txt
models/
└── baseline_classifier/
    ├── logistic_regression_model.pkl
    ├── tfidf_vectorizer.pkl
    ├── metrics.json
    └── label_mapping.json
```

---

# 🎯 Purpose

This folder contains trained machine learning artifacts, vectorizers, metadata, and evaluation outputs used in the Contract Intelligence AI pipeline.

Currently, the folder contains the baseline legal clause classification model developed using:
- TF-IDF Vectorization
- Logistic Regression

The baseline model is used to validate preprocessing quality and establish benchmark performance before transformer-based fine-tuning using Legal-BERT.

---

# 📦 Stored Artifacts

---

# 1️⃣ `logistic_regression_model.pkl`

## Description
Serialized Logistic Regression classifier trained on clause-level legal text snippets.

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
Logistic Regression
    ↓
Binary Classification
```

---

# 2️⃣ `tfidf_vectorizer.pkl`

## Description
Serialized TF-IDF vectorizer fitted on the processed legal clause dataset.

## Purpose
Convert legal text into numerical feature vectors for machine learning models.

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
Stores evaluation metrics and model performance results for the baseline classifier.

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

# 📊 Baseline Model Performance

| Metric | Score |
|---|---|
| Accuracy | 91.4% |
| Precision | 93.9% |
| Recall | 81.9% |
| F1-Score | 87.5% |

---

# 🧠 Key Observations

- Clause-level preprocessing significantly improved performance
- TF-IDF + Logistic Regression provided strong baseline results
- Legal terminology became dominant predictive features
- Full-contract inputs caused severe noise and memorization issues
- Recall remains the most important metric for legal AI reliability

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
- The vectorizer must always be loaded together with the trained classifier
- Metrics and mappings should remain version-aligned with the trained model
- Current models are baseline research/development artifacts
- Not intended for production legal decision-making