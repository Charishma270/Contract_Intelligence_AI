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
- Legal datasets often require extensive preprocessing before model training

---

## 📌 Output

- Dataset understanding
- Label analysis
- Clause inspection
- Dataset structure validation
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
- Exported processed dataset for downstream ML pipelines

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
- Improved feature relevance for downstream classifiers

---

# 3️⃣ `baseline_clause_classifier.ipynb`

## 🎯 Purpose
Train and evaluate a baseline Logistic Regression classifier for legal clause classification before transformer fine-tuning.

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
- Implemented Stratified K-Fold Cross Validation

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

## 📈 Logistic Regression Results

### Hold-Out Evaluation

| Metric | Score |
|---|---|
| Accuracy | 91.4% |
| Precision | 93.9% |
| Recall | 81.9% |
| F1-Score | 87.5% |

---

### Cross Validation Results

| Metric | Mean Score |
|---|---|
| Accuracy | 90.6% |
| Precision | 94.4% |
| Recall | 79.0% |
| F1-Score | 86.0% |

---

## 📌 Key Findings

- Clause-level preprocessing dramatically improved performance
- Model learned legal terminology instead of memorizing company names
- Cross-validation confirmed stable generalization performance
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
- Cross-validation is essential for reliability verification
- Recall is especially important for legal AI systems

---

# 4️⃣ `baseline_clause_classifier_svm.ipynb`

## 🎯 Purpose
Train and evaluate a LinearSVC baseline classifier for legal clause classification and compare performance against Logistic Regression.

---

## ✅ Work Completed

- Reused processed clause classification dataset
- Applied identical preprocessing and TF-IDF configuration
- Trained LinearSVC classifier
- Evaluated:
  - Accuracy
  - Precision
  - Recall
  - F1-score
- Compared model performance against Logistic Regression baseline
- Analyzed reduction in false negatives
- Validated improvement in clause detection reliability

---

## ⚙️ ML Pipeline

```txt
Clause Dataset
    ↓
TF-IDF Vectorization
    ↓
LinearSVC
    ↓
Evaluation Metrics
```

---

## 📊 LinearSVC Results

| Metric | Score |
|---|---|
| Accuracy | 93.9% |
| Precision | 94.9% |
| Recall | 87.9% |
| F1-Score | 91.3% |

---

## 📌 Key Findings

- LinearSVC outperformed Logistic Regression across all evaluation metrics
- Significant recall improvement:
  - 81.9% → 87.9%
- False negatives reduced:
  - 27 → 18
- "Termination For Convenience" classification improved substantially
- SVM margin-based classification handled sparse TF-IDF vectors more effectively

---

## 🧠 Key Learnings

- LinearSVC performs strongly on sparse high-dimensional legal text
- Better margin separation improved clause detection recall
- Strong preprocessing enabled classical ML models to achieve high performance
- Baseline comparisons provide meaningful benchmarks before transformer fine-tuning

---

# 📊 Baseline Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 91.4% | 93.9% | 81.9% | 87.5% |
| LinearSVC | 93.9% | 94.9% | 87.9% | 91.3% |

---

## 🧠 Comparison Summary

- LinearSVC achieved the best overall performance
- Largest improvement observed in recall
- Clause-level preprocessing was the biggest contributor to model improvement
- Classical ML baselines established strong benchmark performance prior to Legal-BERT experimentation

---

## 🚧 Next Planned Steps

- Hyperparameter tuning
- Confidence score calibration
- Legal-BERT tokenizer integration
- Legal-BERT fine-tuning
- Transformer benchmarking
- Inference pipeline development
- API integration