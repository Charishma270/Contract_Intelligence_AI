# ⚖️ Risk Engine

The core analysis and risk scoring module for the Contract Intelligence AI system. It takes raw legal text, runs clause detection through multiple models, and produces explainable risk assessments.

---

## 📂 Directory Structure

```
risk_engine/
│
├── analysis/                         # Clause detection models
│   ├── classifier_inference.py       # SVM single-label classifier (4 labels)
│   ├── legal_bert_inference.py       # Legal-BERT binary classifier
│   ├── multi_label_inference.py      # Multi-label SVM classifier (41 labels)
│   └── multilabel_legal_bert_inference.py  # Multi-label Legal-BERT (41 labels + risk scoring)
│
├── rules/                            # Risk rule definitions
│   └── risk_rules.py                 # RISK_RULES dictionary (41 CUAD labels)
│
├── scoring/                          # Risk computation
│   └── risk_calculator.py            # calculate_risk() function
│
└── README.md
```

---

## 🔄 Pipeline Flow

```
Legal Text (clause snippet)
        │
        ▼
┌───────────────────────────────┐
│  Multi-Label Legal-BERT       │
│  (multilabel_legal_bert_      │
│   inference.py)               │
│                               │
│  ┌─────────────────────────┐  │
│  │ Tokenize → Model →     │  │
│  │ Sigmoid → Threshold     │  │
│  └─────────────────────────┘  │
│        │                      │
│        ▼                      │
│  For each detected label:     │
│  ┌─────────────────────────┐  │
│  │ calculate_risk()        │  │
│  │ (risk_calculator.py)    │  │
│  │     ↓                   │  │
│  │ RISK_RULES lookup       │  │
│  │ (risk_rules.py)         │  │
│  └─────────────────────────┘  │
└───────────────────────────────┘
        │
        ▼
  Structured Output:
  {
    "label": "Uncapped Liability",
    "confidence": 0.91,
    "risk_level": "HIGH",
    "risk_score": 86,
    "reason": "No cap on liability..."
  }
```

---

## 📁 Module Details

### `analysis/` — Clause Detection

Contains inference modules for all trained models. Each module loads its model at import time and exposes a prediction function.

#### `classifier_inference.py`

- **Model**: LinearSVC (single-label, 4 labels)
- **Input**: Raw text
- **Output**: Predicted label name
- **Function**: `classify_clause(text)`

#### `legal_bert_inference.py`

- **Model**: Legal-BERT binary classifier (Termination For Convenience)
- **Input**: Raw text
- **Output**: `{ prediction, confidence, confidence_band }`
- **Function**: `predict_clause_with_legal_bert(text)`

#### `multi_label_inference.py`

- **Model**: OneVsRestClassifier(LinearSVC) — 41 labels
- **Input**: Raw text
- **Output**: List of detected label names
- **Function**: `predict_multi_labels(text)`

#### `multilabel_legal_bert_inference.py` ⭐

- **Model**: Multi-label Legal-BERT — 41 labels
- **Input**: Raw text, optional threshold (default 0.30)
- **Output**: List of detected labels with confidence + risk scoring
- **Function**: `predict_multilabel_legal_bert(text, threshold=0.30)`
- **Risk integration**: Each detected label is enriched with `risk_level`, `risk_score`, and `reason`

---

### `rules/` — Risk Rule Definitions

#### `risk_rules.py`

Contains the `RISK_RULES` dictionary — one entry per CUAD label (41 total).

Each entry has:

| Field | Description |
|---|---|
| `risk_level` | `HIGH`, `MEDIUM`, or `LOW` |
| `base_score` | 0–100 severity score (before confidence adjustment) |
| `reason` | Plain-English explanation for non-lawyers |

**Risk distribution:**

| Level | Count | Examples |
|---|---|---|
| HIGH (10) | Financial/legal exposure | Uncapped Liability, IP Ownership Assignment, Non-Compete |
| MEDIUM (18) | Significant but manageable | Renewal Term, Revenue Sharing, Minimum Commitment |
| LOW (13) | Informational/protective | Termination For Convenience, Governing Law, Parties |

---

### `scoring/` — Risk Computation

#### `risk_calculator.py`

**Function:** `calculate_risk(clause_type, confidence) → dict`

Computes a confidence-adjusted risk score:

```
adjusted_score = base_score × confidence
```

**Example:**

```python
from risk_engine.scoring.risk_calculator import calculate_risk

result = calculate_risk("Uncapped Liability", confidence=0.91)

# {
#     "clause_type":  "Uncapped Liability",
#     "risk_level":   "HIGH",
#     "risk_score":   86,          # 95 × 0.91
#     "confidence":   0.91,
#     "reason":       "No cap on liability exposes the organization
#                      to unlimited financial damages."
# }
```

**Safety:** Unknown clause labels return a default LOW risk rule instead of raising errors.

---

## 📊 Output Format

Each detected clause produces:

```json
{
    "label": "Uncapped Liability",
    "confidence": 0.91,
    "risk_level": "HIGH",
    "risk_score": 86,
    "reason": "No cap on liability exposes the organization to unlimited financial damages."
}
```

| Field | Type | Description |
|---|---|---|
| `label` | string | CUAD clause category name |
| `confidence` | float | Model sigmoid probability (0.0–1.0) |
| `risk_level` | string | HIGH / MEDIUM / LOW |
| `risk_score` | int | 0–100, adjusted by confidence |
| `reason` | string | Plain-English risk explanation |

---

## 🧠 Design Decisions

1. **Rule-based risk scoring** — First-version simplicity. Risk levels and base scores are manually assigned based on legal domain knowledge, not ML-derived. Future versions can learn from review outcomes.

2. **Confidence adjustment** — `risk_score = base_score × confidence`. A HIGH-risk clause detected with low confidence gets a proportionally lower score, preventing false alarm fatigue.

3. **Safe fallback** — Unknown clause labels return a default LOW/10 risk instead of crashing, making the system robust to model output variations.

4. **Separation of concerns** — Rules (`risk_rules.py`) are separate from computation (`risk_calculator.py`) and inference (`multilabel_legal_bert_inference.py`). Each can be updated independently.

5. **All 41 labels covered** — Every CUAD label has a risk mapping. Zero gaps between the model output vocabulary and the risk rules.

---

## 🚧 Future Improvements

- Per-label threshold calibration (different optimal thresholds per clause type)
- Dynamic risk weights learned from user feedback
- Contract-level aggregate risk scoring (overall document risk)
- Temporal risk tracking (risk changes across contract versions)
- Industry-specific risk profiles (healthcare vs tech vs finance)
