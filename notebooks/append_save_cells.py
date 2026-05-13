import json

nb_path = r"C:\Users\chari\Desktop\Contract_Intelligence_AI\notebooks\baseline_clause_classifier.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

def make_md(source, cell_id):
    lines = source.split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": src, "id": cell_id}

def make_code(source, cell_id):
    lines = source.split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None, "id": cell_id}

new_cells = []

new_cells.append(make_md("---\n## Phase 8 — Save Model Artifacts", "md_save_header"))

new_cells.append(make_code("""import joblib
import json
import os

# Define output directory
save_dir = r"C:\\Users\\chari\\Desktop\\Contract_Intelligence_AI\\models\\clause_classifier\\baseline_classifier"
os.makedirs(save_dir, exist_ok=True)

# ==========================================
# 1. Save Logistic Regression Model
# ==========================================
model_path = os.path.join(save_dir, "logistic_regression_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved: {model_path}")

# ==========================================
# 2. Save TF-IDF Vectorizer
# ==========================================
tfidf_path = os.path.join(save_dir, "tfidf_vectorizer.pkl")
joblib.dump(tfidf, tfidf_path)
print(f"Vectorizer saved: {tfidf_path}")

# ==========================================
# 3. Save Label Mapping
# ==========================================
label_mapping = {
    "label_names": sorted(df['label_name'].unique().tolist()),
    "target_mapping": {
        "0": "clause_absent",
        "1": "clause_present"
    },
    "label_distribution": df['label_name'].value_counts().to_dict(),
    "target_distribution": {
        str(k): int(v) for k, v in df['target'].value_counts().items()
    }
}

label_path = os.path.join(save_dir, "label_mapping.json")
with open(label_path, "w") as f:
    json.dump(label_mapping, f, indent=2)
print(f"Label mapping saved: {label_path}")

# ==========================================
# 4. Save Metrics
# ==========================================
per_label_metrics = {}
for label in sorted(df['label_name'].unique()):
    mask = df.loc[test_indices, 'label_name'] == label
    if mask.sum() == 0:
        continue
    y_true_l = y_test[mask]
    y_pred_l = y_pred[mask.values]
    per_label_metrics[label] = {
        "samples": int(mask.sum()),
        "accuracy": round(float(accuracy_score(y_true_l, y_pred_l)), 4),
        "precision": round(float(precision_score(y_true_l, y_pred_l, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true_l, y_pred_l, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true_l, y_pred_l, zero_division=0)), 4)
    }

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

metrics = {
    "model": "LogisticRegression",
    "vectorizer": "TfidfVectorizer",
    "vectorizer_params": {
        "max_features": 10000,
        "ngram_range": [1, 2],
        "stop_words": "english",
        "min_df": 2,
        "max_df": 0.95
    },
    "split": {
        "test_size": 0.20,
        "random_state": 42,
        "stratified": True,
        "train_samples": int(X_train.shape[0]),
        "test_samples": int(X_test.shape[0])
    },
    "overall_metrics": {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4)
    },
    "confusion_matrix": {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp)
    },
    "per_label_metrics": per_label_metrics
}

metrics_path = os.path.join(save_dir, "metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=2)
print(f"Metrics saved: {metrics_path}")

# ==========================================
# VERIFY SAVED FILES
# ==========================================
print("\\n" + "=" * 60)
print("ALL ARTIFACTS SAVED SUCCESSFULLY")
print("=" * 60)
print(f"\\nDirectory: {save_dir}")
print("\\nFiles:")
for fname in os.listdir(save_dir):
    fpath = os.path.join(save_dir, fname)
    size_kb = os.path.getsize(fpath) / 1024
    print(f"  {fname:35s} {size_kb:>8.1f} KB")""", "code_save_artifacts"))

nb["cells"].extend(new_cells)

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Added {len(new_cells)} cells to notebook")
