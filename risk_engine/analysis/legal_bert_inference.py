from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

import torch


# Model path
MODEL_PATH = (
    "models/legal_bert_classifier/model"
)

# Tokenizer path
TOKENIZER_PATH = (
    "models/legal_bert_classifier/tokenizer"
)


print("\nLoading Legal-BERT model...\n")


# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    TOKENIZER_PATH
)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

# Evaluation mode
model.eval()

print("Legal-BERT loaded successfully!\n")


def predict_clause_with_legal_bert(text):

    # Tokenize text
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    # Disable gradients
    with torch.no_grad():

        outputs = model(**inputs)

    # Convert logits to probabilities
    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )

    # Prediction index
    predicted_class = torch.argmax(
        probabilities,
        dim=1
    ).item()

    # Confidence score
    confidence = torch.max(
        probabilities
    ).item()

    # Binary mapping
    if predicted_class == 1:

        prediction = (
            "Termination For Convenience"
        )

    else:

        prediction = "Other Clause"

    return {

        "prediction": prediction,

        "confidence": round(
            confidence,
            4
        )
    }