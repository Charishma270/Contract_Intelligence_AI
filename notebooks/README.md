# 📘 Notebook Documentation

---

# 1️⃣ `cuad_exploration.ipynb`

## 🎯 Purpose
Initial exploration and understanding of the CUAD (Contract Understanding Atticus Dataset) structure.

---

## ✅ Work Completed

- Loaded `CUAD_v1.json`
- Explored dataset hierarchy
- Inspected contract structure
- Parsed paragraphs and QA annotations
- Extracted all 41 legal clause categories
- Analyzed possible vs impossible samples
- Identified target labels for classification:
  - Termination For Convenience
  - Renewal Term
  - Cap On Liability
  - Uncapped Liability
- Inspected real clause examples and answer spans

---

## 🧠 Key Learnings

- CUAD follows a legal Question Answering (QA) format
- Contracts are divided into paragraphs
- Each paragraph contains legal Q&A annotations
- `is_impossible=True` indicates absence of a clause

---

## 📌 Output

- Dataset understanding
- Label analysis
- Clause inspection
- Preprocessing strategy planning

---

# 2️⃣ `clause_classification_dataset.ipynb`

## 🎯 Purpose
Convert the CUAD legal QA dataset into a binary clause classification dataset suitable for ML and Legal-BERT fine-tuning.

---

## ✅ Work Completed

- Loaded and processed CUAD dataset
- Selected 4 target legal clause categories
- Built clause-level extraction pipeline
- Extracted:
  - positive clause samples
  - negative clause samples
- Implemented contextual clause extraction
- Reduced dataset size significantly by avoiding full-contract duplication
- Generated structured classification dataset

---

## 📊 Dataset Format

| text | label_name | target |
|---|---|---|
| clause snippet | Termination For Convenience | 1 |
| unrelated snippet | Cap On Liability | 0 |

---

## ⚙️ Optimizations Implemented

### Positive Samples
- answer span + surrounding context

### Negative Samples
- random contextual excerpts

### Dataset Optimization
- reduced CSV size:
  - ~107 MB → ~1.3 MB

---

## 📂 Generated Outputs

- `clause_classification_dataset.csv`
- preprocessing pipeline notebook
- standalone preprocessing script

---

## 🚧 Next Planned Steps

- Baseline ML classifier
- TF-IDF vectorization
- Logistic Regression evaluation
- Legal-BERT fine-tuning
- Tokenizer pipeline development