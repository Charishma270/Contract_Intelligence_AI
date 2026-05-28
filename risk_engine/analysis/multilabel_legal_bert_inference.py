from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

import torch
import json

from risk_engine.scoring.risk_calculator import (
    calculate_risk
)



# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

MODEL_PATH = (
    "models/legal_bert_multilabel/"
    "trained_model"
)

TOKENIZER_PATH = (
    "models/legal_bert_multilabel/"
    "tokenizer"
)

LABEL_MAP_PATH = (
    "models/legal_bert_multilabel/"
    "label_mapping.json"
)


# ---------------------------------------------------------
# Load tokenizer + model
# ---------------------------------------------------------

print(
    "\nLoading Multi-Label Legal-BERT model...\n"
)

tokenizer = AutoTokenizer.from_pretrained(
    TOKENIZER_PATH
)

model = (
    AutoModelForSequenceClassification
    .from_pretrained(MODEL_PATH)
)

model.eval()


# ---------------------------------------------------------
# Load label mapping
# ---------------------------------------------------------

with open(LABEL_MAP_PATH, "r") as f:

    label_mapping = json.load(f)

index_to_label = (
    label_mapping["index_to_label"]
)

print(
    "Multi-Label Legal-BERT loaded successfully!\n"
)


# ---------------------------------------------------------
# Multi-label prediction
# ---------------------------------------------------------

def predict_multilabel_legal_bert(

    text,
    threshold=0.30
):

    inputs = tokenizer(

        text,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=256
    )

    with torch.no_grad():

        outputs = model(**inputs)

    logits = outputs.logits

    probabilities = torch.sigmoid(
        logits
    )[0]

    detected_labels = []

    # -----------------------------------------------------
    # Convert probabilities into labels + risk scores
    # -----------------------------------------------------

    for idx, probability in enumerate(
        probabilities
    ):

        probability = probability.item()

        if probability >= threshold:

            label_name = (
                index_to_label.get(
                    str(idx),
                    f"Label_{idx}"
                )
            )

            # -------------------------------------------------
            # Risk scoring: enrich each detection with
            # risk_level, risk_score, and reason
            # -------------------------------------------------

            risk_info = calculate_risk(
                clause_type=label_name,
                confidence=probability,
            )

            detected_labels.append({

                "label":
                    label_name,

                "confidence":
                    round(probability, 4),

                "risk_level":
                    risk_info["risk_level"],

                "risk_score":
                    risk_info["risk_score"],

                "reason":
                    risk_info["reason"],
            })

    # -----------------------------------------------------
    # Sort labels by confidence
    # -----------------------------------------------------

    detected_labels = sorted(

        detected_labels,

        key=lambda x: x["confidence"],

        reverse=True
    )

    return detected_labels

