from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="theatticusproject/cuad",
    repo_type="dataset",
    local_dir="data/raw/dataset",
    local_dir_use_symlinks=False
)

print("CUAD dataset downloaded successfully!")