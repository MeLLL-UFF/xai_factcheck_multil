import subprocess

checkpoint_path = "G:\\GitHub\\apps\\mestrado\\CONCRETE\\checkpoints\\concrete_best_zershot.pt"
test_path = "G:\\GitHub\\apps\\mestrado\\CONCRETE\\data\\x-fact\\zeroshot.tsv"

command = [
    "python",
     "G:\\GitHub\\apps\\mestrado\\CONCRETE\\src\\test.py",
    "--checkpoint_path",checkpoint_path,
    "--test_path",test_path,
    "--model_name", "bert-base-multilingual-cased",
    "--retrieval_dir", "G:\\GitHub\\apps\\mestrado\\CONCRETE\\CORA\\mDPR\\retrieved_docs",
    ]

subprocess.run(command)
