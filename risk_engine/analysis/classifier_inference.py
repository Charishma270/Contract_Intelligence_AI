import joblib
import json

# Load trained SVM classifier
model = joblib.load(
    "models/clause_classifier/svm_classifier/svm_model.pkl"
)

# Load TF-IDF vectorizer
vectorizer = joblib.load(
    "models/clause_classifier/svm_classifier/tfidf_vectorizer.pkl"
)

# Load label metadata
with open(
    "models/clause_classifier/svm_classifier/label_mapping.json",
    "r"
) as f:

    label_metadata = json.load(f)

# Extract ordered label list
label_names = label_metadata["label_names"]


def classify_clause(text):

    # Convert text to TF-IDF vector
    vector = vectorizer.transform([text])

    # Predict numeric class
    prediction = model.predict(vector)[0]

    # Convert prediction ID → label
    predicted_label = label_names[prediction]

    return predicted_label