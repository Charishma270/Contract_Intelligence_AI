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

## 📌 Final Dataset Statistics

| Property | Value |
|---|---|
| Total Samples | 2040 |
| Labels | 4 |
| Positive Samples | 745 |
| Negative Samples | 1295 |
| Average Text Length | ~638 characters |

---

## 🧠 Key Improvements

- Replaced full-contract inputs with clause-level contextual snippets
- Reduced dataset noise significantly
- Improved ML suitability for classification tasks
- Prevented model memorization of company names

---

# 3️⃣ `baseline_clause_classifier.ipynb`

## 🎯 Purpose
Train and evaluate a baseline machine learning model for legal clause classification before transformer fine-tuning.

---

## ✅ Work Completed

- Loaded processed classification dataset
- Performed dataset validation and inspection
- Applied train/test split using stratified sampling
- Implemented TF-IDF vectorization
- Trained Logistic Regression classifier
- Evaluated model performance using:
  - Accuracy
  - Precision
  - Recall
  - F1-score
- Analyzed confusion matrix
- Performed feature importance analysis
- Compared preprocessing impact before vs after clause-level extraction

---

## ⚙️ ML Pipeline

```txt
Clause Dataset
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression
    ↓
Evaluation Metrics
```

---

## 📊 TF-IDF Configuration

| Parameter | Value |
|---|---|
| Max Features | 10,000 |
| N-Grams | Unigrams + Bigrams |
| Stop Words | English |
| Min DF | 2 |
| Max DF | 0.95 |

---

## 📈 Baseline Model Results

| Metric | Score |
|---|---|
| Accuracy | 91.4% |
| Precision | 93.9% |
| Recall | 81.9% |
| F1-Score | 87.5% |

---

## 📌 Key Findings

- Clause-level preprocessing dramatically improved performance
- Model learned legal terminology instead of memorizing company names
- Most predictive features:
  - liability
  - termination
  - damages
  - notice
  - terminate agreement
- Main weakness:
  - lower recall for "Termination For Convenience"

---

## 📂 Saved Outputs

- `logistic_regression_model.pkl`
- `tfidf_vectorizer.pkl`
- `metrics.json`
- `label_mapping.json`

Stored inside:
```txt
models/baseline_classifier/
```

---

## 🧠 Key Learnings

- Preprocessing quality strongly affects NLP model performance
- Clause-level contextual snippets outperform full-contract inputs
- Baseline ML models provide critical validation before transformer fine-tuning
- Recall is especially important for legal AI systems

---

## 🚧 Next Planned Steps

- Cross-validation experiments
- SVM baseline comparison
- Hyperparameter tuning
- Legal-BERT tokenizer integration
- Legal-BERT fine-tuning
- Inference pipeline development
- API integration