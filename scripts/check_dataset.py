import pandas as pd

df = pd.read_csv("data/processed/clause_classification_dataset.csv")

print("\nColumns:\n")
print(df.columns)

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nDataset Shape:\n")
print(df.shape)