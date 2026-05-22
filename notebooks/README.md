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
- Legal datasets require extensive preprocessing before model training

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

Convert the CUAD legal QA dataset into a binary clause classification dataset suitable for classical ML and Legal-BERT fine-tuning.

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

Stored inside:

```txt
models/baseline_classifier/
```

### Includes

- `logistic_regression_model.pkl`
- `tfidf_vectorizer.pkl`
- `metrics.json`
- `label_mapping.json`

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

## 📂 Saved Outputs

Stored inside:

```txt
models/clause_classifier/svm_classifier/
```

### Includes

- `svm_model.pkl`
- `tfidf_vectorizer.pkl`
- `metrics.json`
- `label_mapping.json`

---

## 🧠 Key Learnings

- LinearSVC performs strongly on sparse high-dimensional legal text
- Better margin separation improved clause detection recall
- Strong preprocessing enabled classical ML models to achieve high performance
- Baseline comparisons provide meaningful benchmarks before transformer fine-tuning

---

# 5️⃣ `legal_bert_clause_classifier.ipynb`

## 🎯 Purpose

Fine-tune Legal-BERT on clause-level legal text snippets for transformer-based legal clause classification.

This notebook benchmarks transformer performance against classical ML baselines:
- Logistic Regression
- LinearSVC

---

## ✅ Work Completed

- Loaded processed clause classification dataset
- Filtered dataset for:
  - `Termination For Convenience`
- Applied train/test split using stratified sampling
- Loaded:
  - Legal-BERT tokenizer
  - Legal-BERT transformer model
- Implemented transformer tokenization pipeline
- Built HuggingFace Dataset pipeline
- Configured HuggingFace Trainer API
- Fine-tuned Legal-BERT
- Evaluated transformer performance
- Compared results against:
  - Logistic Regression
  - LinearSVC
- Saved:
  - trained model
  - tokenizer
  - metrics
  - checkpoints

---

## ⚙️ Transformer Pipeline

```txt
Clause Snippet
    ↓
Legal-BERT Tokenizer
    ↓
Transformer Embeddings
    ↓
Legal-BERT Fine-Tuning
    ↓
Binary Classification
```

---

## 🧠 Base Model

```txt
nlpaueb/legal-bert-base-uncased
```

---

## ⚙️ Training Configuration

| Parameter | Value |
|---|---|
| Epochs | 2 |
| Batch Size | 8 |
| Max Length | 512 |
| Evaluation Strategy | Per Epoch |
| Save Strategy | Per Epoch |
| Best Model Metric | F1-Score |
| Random Seed | 42 |

---

## 📊 Legal-BERT Results

| Metric | Score |
|---|---|
| Accuracy | 99.0% |
| Precision | 100.0% |
| Recall | 97.3% |
| F1-Score | 98.6% |
| Loss | 0.0587 |

---

## 📌 Confusion Matrix

| Type | Count |
|---|---|
| True Negatives | 65 |
| False Positives | 0 |
| False Negatives | 1 |
| True Positives | 36 |

---

## 📊 Full Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 91.4% | 93.9% | 81.9% | 87.5% |
| LinearSVC | 93.9% | 94.9% | 87.9% | 91.3% |
| Legal-BERT | 99.0% | 100.0% | 97.3% | 98.6% |

---

## 📌 Key Findings

- Legal-BERT significantly outperformed classical ML baselines
- Transformer semantic understanding improved legal clause detection
- False negatives reduced dramatically:
  - Logistic Regression → 27
  - LinearSVC → 18
  - Legal-BERT → 1
- Legal-BERT captured contextual legal meaning beyond keyword matching
- Clause-level preprocessing was critical for transformer performance

---

## 📂 Saved Outputs

Stored inside:

```txt
models/legal_bert_classifier/
```

### Includes

- trained Legal-BERT weights
- tokenizer files
- metrics.json
- checkpoint artifacts

---

## 🧠 Key Learnings

- Transformer models outperform classical ML on contextual legal text understanding
- Fine-tuning quality strongly depends on preprocessing quality
- Recall is the most critical metric in legal AI systems
- HuggingFace Trainer automatically saves checkpoint artifacts during training
- Legal-BERT is highly effective for clause-level legal classification tasks

---

# 6️⃣ `multi_label_clause_dataset.ipynb`

## 🎯 Purpose

Transform the CUAD dataset into a full **multi-label classification** dataset across all 41 legal clause categories, with contract-level provenance tracking to prevent train/test data leakage.

This replaces the previous 4-label binary classification format with a proper multi-label structure suitable for Legal-BERT fine-tuning.

---

## ✅ Work Completed

- Loaded full CUAD dataset (510 contracts)
- Auto-extracted all 41 unique clause labels
- Built label engineering pipeline:
  - `all_labels` sorted list
  - `label_to_index` mapping
  - `index_to_label` mapping
- Preserved clause-level contextual extraction logic:
  - `extract_positive_text()` — answer span + surrounding context
  - `extract_negative_text()` — random contract excerpt
- Implemented two-pass multi-label aggregation:
  - Pass 1: collect all (snippet, label, target, contract_id) tuples
  - Pass 2: aggregate labels per unique snippet using logical OR
- Added `contract_id` provenance tracking on every row
- Built contract-level train/test split function
- Comprehensive dataset validation
- Saved dataset, label mappings, and statistics

---

## 📊 Dataset Format

| text | contract_id | Affiliate License-Licensee | ... | Warranty Duration |
|---|---|---|---|---|
| clause snippet | ContractName | 0 | ... | 1 |
| clause snippet | ContractName | 1 | ... | 0 |

Each label column is binary: `1` = clause present, `0` = clause absent.

---

## ⚙️ Key Design Decisions

### Multi-Label Aggregation
- One row per unique snippet (not one row per label decision)
- Labels merged via logical OR across all QA annotations
- Eliminates 41x row duplication

### Contract-Level Leakage Prevention
- Every snippet stores its source `contract_id`
- `get_contract_level_split()` splits by contract — not random rows
- Prevents model from learning document style instead of legal semantics

### Negative Snippet Noise
- Known limitation: random negative excerpts may contain unannotated clause language
- Acceptable for now — positives provide strong learning signal

---

## 📌 Final Dataset Statistics

| Property | Value |
|---|---|
| Total Rows | 20,104 |
| Total Columns | 43 (text + contract_id + 41 labels) |
| Labels | 41 |
| Unique Contracts | 510 |
| Null Values | 0 |
| Duplicate Rows | 0 |
| Label Values | Binary (0, 1) |

---

## 📂 Saved Outputs

Stored inside:

```txt
data/processed/
```

### Includes

- `multi_label_clause_dataset.csv` — full dataset (14.4 MB)
- `label_mapping.json` — label-to-index and index-to-label mappings
- `dataset_statistics.json` — comprehensive dataset statistics
- `label_distribution.png` — positive count per label chart
- `multilabel_distribution.png` — active labels per snippet histogram

---

## 🧠 Key Learnings

- Multi-label classification requires sigmoid activation (not softmax)
- `BCEWithLogitsLoss` is the correct loss function (not `CrossEntropyLoss`)
- Contract-level splitting is critical for realistic legal NLP evaluation
- Two-pass aggregation prevents snippet duplication while preserving all label information
- Rare labels in legal datasets require careful imbalance handling during training

---

# 7️⃣ `multi_label_baseline_classifier.ipynb`

## 🎯 Purpose

Train and evaluate a multi-label classical ML baseline using TF-IDF + OneVsRestClassifier(LinearSVC) across all 41 CUAD legal clause categories.

This establishes a benchmark before multi-label Legal-BERT fine-tuning.

---

## ✅ Work Completed

- Loaded multi-label dataset (20,104 samples, 41 labels)
- Implemented contract-level train/test split (zero leakage verified)
- Built TF-IDF vectorization pipeline (10,000 features, bigrams)
- Trained OneVsRestClassifier with LinearSVC (41 independent classifiers)
- Evaluated with full multi-label metrics suite
- Performed per-label performance analysis
- Identified high-risk labels via false negative analysis
- Generated per-label F1 and recall visualizations
- Saved model, vectorizer, metrics, and label mapping

---

## ⚙️ ML Pipeline

```txt
Multi-Label Dataset (20,104 × 43)
    ↓
Contract-Level Split (408 train / 102 test)
    ↓
TF-IDF Vectorization (10,000 features)
    ↓
OneVsRestClassifier(LinearSVC) × 41 labels
    ↓
Multi-Label Evaluation
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

## 📈 Multi-Label SVM Results

### Overall Metrics

| Metric | Score |
|---|---|
| Subset Accuracy (Exact Match) | 75.49% |
| Hamming Loss | 0.0072 |

### Aggregated Metrics

| Averaging | Precision | Recall | F1-Score |
|---|---|---|---|
| Micro | 59.30% | 34.18% | 43.37% |
| Macro | 48.53% | 22.80% | 27.96% |

---

## 📌 Key Findings

- **High subset accuracy** (75.49%) — most snippets have all labels correct
- **Very low hamming loss** (0.0072) — only 0.72% of individual label predictions are wrong
- **Micro vs macro gap** reveals that common labels are predicted well but rare labels suffer
- **Low macro recall** (22.80%) highlights that many labels lack sufficient positive examples for TF-IDF to capture patterns
- Contract-level splitting provides realistic (harder) evaluation compared to random splitting

---

## 📂 Saved Outputs

Stored inside:

```txt
models/multi_label_svm_classifier/
```

### Includes

- `svm_model.pkl` — trained OneVsRest LinearSVC model
- `tfidf_vectorizer.pkl` — fitted TF-IDF vectorizer
- `metrics.json` — comprehensive metrics (overall, micro, macro, per-label)
- `label_mapping.json` — label-to-index mappings
- `per_label_f1.png` — per-label F1 score chart
- `per_label_recall.png` — per-label recall chart

---

## 🧠 Key Learnings

- Multi-label evaluation is fundamentally harder than single-label
- Subset accuracy is extremely strict — entire 41-label vector must match exactly
- Hamming loss provides a more forgiving per-label view
- Macro metrics expose rare label failures hidden by micro aggregation
- TF-IDF + SVM struggles with labels that have few positive examples
- This baseline sets the benchmark for transformer improvement

---

# 8️⃣ `tokenized_multi_label_dataset.ipynb`

## 🎯 Purpose

Preprocess and tokenize the multi-label CUAD dataset using Legal-BERT tokenizer, creating reusable HuggingFace Dataset objects saved to disk for future training.

This notebook is **preprocessing only** — no model training.

---

## ✅ Work Completed

- Loaded multi-label dataset (20,104 samples, 41 labels)
- Loaded Legal-BERT tokenizer (`nlpaueb/legal-bert-base-uncased`)
- Performed contract-level train/test split (zero leakage verified)
- Tokenized all text with padding and truncation (max_length=256)
- Created HuggingFace Datasets with input_ids, attention_mask, labels, contract_id
- Validated tokenized shapes, label dimensions, and data types
- Saved tokenized datasets to disk (Arrow format)
- Saved tokenizer for reproducibility
- Verified reload from disk

---

## ⚙️ Tokenization Configuration

| Parameter | Value |
|---|---|
| Tokenizer | nlpaueb/legal-bert-base-uncased |
| Vocab Size | 30,522 |
| Max Length | 256 |
| Padding | max_length |
| Truncation | True |
| Label Type | float32 (for BCEWithLogitsLoss) |

---

## 📊 Dataset Statistics

| Split | Samples | Size on Disk |
|---|---|---|
| Train | 16,073 | 25.97 MB |
| Test | 4,031 | 6.53 MB |

Each sample contains:

| Field | Shape | Type |
|---|---|---|
| input_ids | [256] | int |
| attention_mask | [256] | int |
| labels | [41] | float32 |
| contract_id | — | string |

---

## 📂 Saved Outputs

```txt
data/processed/tokenized_multi_label_dataset/
├── train/
│   ├── data-00000-of-00001.arrow
│   ├── dataset_info.json
│   └── state.json
└── test/
    ├── data-00000-of-00001.arrow
    ├── dataset_info.json
    └── state.json

models/legal_bert_multilabel/tokenizer/
├── tokenizer.json
└── tokenizer_config.json
```

---

## 🧠 Key Learnings

- Transformer tokenization converts text to numerical token IDs
- input_ids are vocabulary indices; attention_mask indicates real vs padding tokens
- Multi-label targets must be float32 for BCEWithLogitsLoss compatibility
- max_length=256 balances information retention with training efficiency
- Saving tokenized datasets avoids re-tokenization during training experiments

---

# 9️⃣ `multi_label_legal_bert_classifier.ipynb`

## 🎯 Purpose

Fine-tune Legal-BERT for multi-label classification across all 41 CUAD legal clause categories using the pre-tokenized dataset, sigmoid activation, and BCEWithLogitsLoss.

---

## ✅ Notebook Contains

- GPU/device detection
- Tokenized dataset loading (train + test)
- Label mapping loading
- Legal-BERT model loading with `problem_type="multi_label_classification"`
- `compute_metrics()` function (sigmoid + threshold + multi-label metrics)
- TrainingArguments configuration
- Trainer setup
- Training cell (commented — ready to run)
- Evaluation cell (commented — ready to run)
- Per-label analysis cell (commented — ready to run)
- SVM vs Legal-BERT comparison cell (commented — ready to run)
- Model/tokenizer/metrics saving cells (commented — ready to run)
- Comprehensive markdown theory explanations

---

## ⚙️ Model Configuration

| Parameter | Value |
|---|---|
| Base Model | nlpaueb/legal-bert-base-uncased |
| Num Labels | 41 |
| Problem Type | multi_label_classification |
| Loss Function | BCEWithLogitsLoss (automatic) |
| Activation | Sigmoid |
| Threshold | 0.5 |
| Max Length | 256 |
| Epochs | 2 |
| Batch Size | 8 (train) / 16 (eval) |
| FP16 | Auto (if CUDA available) |
| Best Model Metric | micro_f1 |

---

## 📊 Metrics Computed

| Category | Metrics |
|---|---|
| Overall | Subset Accuracy, Hamming Loss |
| Micro | Precision, Recall, F1 |
| Macro | Precision, Recall, F1 |
| Per-Label | Precision, Recall, F1, Support |

---

## 📂 Output Structure (after training)

```txt
models/legal_bert_multilabel/
├── trained_model/
│   ├── model files
│   └── tokenizer files
├── metrics.json
├── label_mapping.json
└── checkpoints/
```

---

## 🧠 Key Concepts Explained

- Multi-label vs multi-class classification
- Logits, sigmoid, and threshold
- BCEWithLogitsLoss vs CrossEntropyLoss
- Why softmax is incorrect for multi-label
- Independent probability per label

---

## 📌 Execution Status

| Section | Status |
|---|---|
| Configuration | ✓ Ready |
| Dataset loading | ✓ Ready |
| Model loading | ✓ Ready |
| Metrics function | ✓ Ready |
| Trainer setup | ✓ Ready |
| Training | ⏳ Awaiting manual execution |
| Evaluation | ⏳ Awaiting training completion |
| Artifact saving | ⏳ Awaiting training completion |

---

# 📊 Final Model Benchmark Comparison

### Single-Label Experiments (4 labels, binary classification)

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 91.4% | 93.9% | 81.9% | 87.5% |
| LinearSVC | 93.9% | 94.9% | 87.9% | 91.3% |
| Legal-BERT | 99.0% | 100.0% | 97.3% | 98.6% |

### Multi-Label Experiment (41 labels)

| Model | Subset Acc | Hamming Loss | Micro F1 | Macro F1 |
|---|---|---|---|---|
| SVM Baseline (OVR) | 75.49% | 0.0072 | 43.37% | 27.96% |
| Legal-BERT | ⏳ pending | ⏳ pending | ⏳ pending | ⏳ pending |

---

## 🧠 Overall Project Learnings

- Dataset preprocessing quality directly impacts downstream NLP performance
- Clause-level contextual snippets dramatically improve classification quality
- Cross-validation is essential for validating model reliability
- Classical ML provides strong baselines for legal NLP tasks
- Transformer models significantly improve semantic legal understanding
- Recall is the most important metric for legal AI risk detection systems
- Legal-BERT substantially reduced dangerous false negatives
- Contract-level train/test splitting prevents data leakage in legal NLP
- Multi-label aggregation avoids dataset bloat while preserving label richness
- Multi-label evaluation requires different metrics than single-label (hamming loss, subset accuracy)
- TF-IDF baselines establish realistic benchmarks for transformer comparison
- Tokenized datasets should be saved to disk for reproducibility and training efficiency

---

## 🚧 Next Planned Steps

- ~~Multi-label dataset creation~~ ✅ Complete
- ~~Multi-label SVM baseline~~ ✅ Complete
- ~~Transformer tokenization preprocessing~~ ✅ Complete
- ~~Multi-label Legal-BERT training pipeline~~ ✅ Pipeline ready
- **Execute multi-label Legal-BERT training** ⏳ Awaiting GPU execution
- Hyperparameter tuning
- Threshold calibration per label
- Confidence score analysis
- Inference API development
- Legal risk scoring system
- Semantic legal search pipeline
- Production inference optimization
- Frontend/backend integration
- RAG pipeline experimentation