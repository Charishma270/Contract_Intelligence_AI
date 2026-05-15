import json

nb_path = r"C:\Users\chari\Desktop\Contract_Intelligence_AI\notebooks\legal_bert_clause_classifier.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Find and fix the training config cell
for c in nb['cells']:
    if c.get('id') == 'code_training_config':
        src = ''.join(c['source'])
        src = src.replace('no_cuda=True', 'use_cpu=True')
        lines = src.split("\n")
        c['source'] = [l + "\n" for l in lines[:-1]] + [lines[-1]]
        c['outputs'] = []
        c['execution_count'] = None
        print("Fixed: no_cuda -> use_cpu")
        break

# Clear all outputs
for c in nb['cells']:
    if c['cell_type'] == 'code':
        c['outputs'] = []
        c['execution_count'] = None

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook updated and outputs cleared.")
