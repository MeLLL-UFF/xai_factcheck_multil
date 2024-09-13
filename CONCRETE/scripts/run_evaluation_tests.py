import subprocess

checkpoint_path = "G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\checkpoints\\concrete_best_zershot.pt"
test_path = "G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\data\\x-fact\\zeroshot.tsv"
command = [
    "python",
     "G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\src\\test.py",
    "--checkpoint_path",checkpoint_path,
    "--test_path",test_path,
    "--model_name", "bert-base-multilingual-cased",
    "--retrieval_dir", "G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\CORA\\mDPR\\retrieved_docs",
    ]

subprocess.run(command)
