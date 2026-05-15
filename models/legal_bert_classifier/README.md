# 🤖 Legal-BERT Classifier Documentation

---

# 📂 Folder Structure

```txt
models/
└── legal_bert_classifier/
    ├── model/
    │   ├── config.json
    │   └── model.safetensors
    │
    ├── tokenizer/
    │   ├── tokenizer.json
    │   └── tokenizer_config.json
    │
    ├── metrics.json
    └── README.md
```

---

# 🎯 Purpose

This folder contains the fine-tuned Legal-BERT transformer model developed for legal clause classification using the CUAD dataset.

The model was trained to detect whether a target legal clause is:

- present (`1`)
- absent (`0`)

inside legal contract text snippets.

---

# 🧠 Base Model

```txt
nlpaueb/legal-bert-base-uncased
```

Legal-BERT is a transformer model pre-trained on legal documents and legal-domain text.

---

# ⚙️ Fine-Tuning Task

## Target Clause

```txt
Termination For Convenience
```

## Classification Type

Binary Classification

| Label | Meaning |
| ----- | -------- |
| 0 | Clause Absent |
| 1 | Clause Present |

---

# 📦 Stored Artifacts

---

# 1️⃣ `model/`

## Description

Contains the trained transformer model weights and architecture configuration.

## Files

| File | Purpose |
| ----- | -------- |
| `config.json` | Model architecture configuration |
| `model.safetensors` | Trained Legal-BERT weights |

## Purpose

Used for:

- inference
- prediction
- deployment
- future fine-tuning

---

# 2️⃣ `tokenizer/`

## Description

Contains tokenizer configuration and vocabulary used during training.

## Files

| File | Purpose |
| ----- | -------- |
| `tokenizer.json` | Tokenization vocabulary and rules |
| `tokenizer_config.json` | Tokenizer configuration |

## Purpose

Converts raw legal text into tokenized transformer input format.

---

# 3️⃣ `metrics.json`

## Description

Stores evaluation metrics and training configuration for the fine-tuned model.

## Includes

- accuracy
- precision
- recall
- F1-score
- confusion matrix
- dataset split information
- training configuration

---

# 📊 Final Evaluation Results

| Metric | Score |
| ----- | ------ |
| Accuracy | 99.0% |
| Precision | 100.0% |
| Recall | 97.3% |
| F1-Score | 98.6% |
| Loss | 0.0587 |

---

# 📌 Confusion Matrix

| Type | Count |
| ----- | ----- |
| True Negatives | 65 |
| False Positives | 0 |
| False Negatives | 1 |
| True Positives | 36 |

---

# ⚔️ Baseline Comparison

| Model | Accuracy | Precision | Recall | F1 |
| ----- | -------- | --------- | ------ | ---- |
| Logistic Regression | 91.4% | 93.9% | 81.9% | 87.5% |
| LinearSVC | 93.9% | 94.9% | 87.9% | 91.3% |
| Legal-BERT | 99.0% | 100.0% | 97.3% | 98.6% |

---

# 🧠 Key Observations

- Legal-BERT significantly outperformed classical ML baselines
- Transformer-based semantic understanding improved clause detection accuracy
- False negatives reduced dramatically compared to baseline models
- Clause-level preprocessing greatly improved model learning quality
- Legal terminology and contextual understanding became stronger predictive signals

---

# ⚙️ Training Configuration

| Parameter | Value |
| ----- | --------- |
| Epochs | 2 |
| Batch Size | 8 |
| Max Length | 512 |
| Evaluation Strategy | Per Epoch |
| Save Strategy | Per Epoch |
| Best Model Metric | F1-Score |

---

# 🚀 Loading the Model

```python
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

model_path = r"models/legal_bert_classifier/model"
tokenizer_path = r"models/legal_bert_classifier/tokenizer"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

model = AutoModelForSequenceClassification.from_pretrained(model_path)

print("Model loaded successfully!")
```

---

# ⚠️ Important Notes

- The tokenizer must always be loaded together with the model
- `model.safetensors` contains the trained transformer weights
- Checkpoint folders are training artifacts and are not required for inference
- This model currently supports only:

  - `Termination For Convenience`

- Future work includes:

  - multi-label classification
  - all 41 CUAD labels
  - risk scoring integration
  - API deployment
  - legal clause extraction pipeline

---

# 🚧 Planned Future Improvements

- Fine-tuning on all 41 CUAD labels
- Multi-label transformer classification
- Hyperparameter tuning
- Inference API development
- Risk scoring engine integration
- Semantic legal search pipeline
- Legal contract summarization