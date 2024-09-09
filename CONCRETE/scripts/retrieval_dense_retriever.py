import subprocess

file_list = ['train.all', 'dev.all', 'test.all', 'ood', 'zeroshot']

model_file = "G:\\GitHub\\apps\\mestrado\\CONCRETE\\checkpoints\\xICT_biencoder.pt.37-002.9188"
ctx_file = f"G:\\GitHub\\apps\\mestrado\\CONCRETE\\data\\bbc_passages"
encoded_dir = f"G:\\GitHub\\apps\\mestrado\\CONCRETE\\CORA\\mDPR\\embeddings_multilingual"
batch_size = 64
n_docs = 100

for f in file_list:
    claim_file = f"G:\\GitHub\\apps\\mestrado\\CONCRETE\\data\\x-fact\\{f}.tsv"
    out_file = f"G:\\GitHub\\apps\\mestrado\\CONCRETE\\CORA\\mDPR\\retrieved_docs\\{f}.xict.json"
    
    command = [
        "python3", "G:\\GitHub\\apps\\mestrado\\CONCRETE\\CORA\\mDPR\\dense_retriever.py",
        "--model_file", model_file,
        "--ctx_file", ctx_file,
        "--claim_file", claim_file,
        "--encoded_dir", encoded_dir,
        "--out_file", out_file,
        "--batch_size", str(batch_size),
        "--n-docs", str(n_docs)
    ]
    
    subprocess.run(command, check=True)