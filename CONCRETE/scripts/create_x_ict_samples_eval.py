import subprocess

passage_dir = r"G:\GitHub\apps\mestrado\CONCRETE\data\bbc_passages"
out_file = r"G:\GitHub\apps\mestrado\CONCRETE\data\all_ict_samples-trans100.jsonl"

command = [
    "python",
     r"G:\GitHub\apps\mestrado\CONCRETE\CORA\mDPR\create_ict_samples.py",
    "--passage_dir",passage_dir,
    "--out_file",out_file,
    "--num_shards", "4",
    "--shard_id", "3",
    "--is_eval"
    ]

subprocess.run(command)