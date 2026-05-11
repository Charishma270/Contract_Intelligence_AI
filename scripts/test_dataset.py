from datasets import load_dataset

dataset = load_dataset(
    "theatticusproject/cuad",
    split="train",
    streaming=True
)

for sample in dataset.take(1):
    print(sample)