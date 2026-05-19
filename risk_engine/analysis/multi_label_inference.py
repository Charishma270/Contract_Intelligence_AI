import json
import joblib


MODEL_PATH = (
    "models/multi_label_svm_classifier/"
    "svm_model.pkl"
)

VECTORIZER_PATH = (
    "models/multi_label_svm_classifier/"
    "tfidf_vectorizer.pkl"
)

LABEL_MAP_PATH = (
    "models/multi_label_svm_classifier/"
    "label_mapping.json"
)


print("\nLoading Multi-Label SVM model...\n")

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

with open(LABEL_MAP_PATH, "r") as f:

    label_mapping = json.load(f)

print(
    "Multi-Label SVM loaded successfully!\n"
)


def predict_multi_labels(text):

    vector = vectorizer.transform([text])

    predictions = model.predict(vector)[0]

    detected_labels = []

    for idx, value in enumerate(predictions):

        if value == 1:

            # Safe label lookup
            label_name = label_mapping.get(
                str(idx)
            )

            # Skip missing labels safely
            if label_name:

                detected_labels.append(
                    label_name
                )

    return detected_labels