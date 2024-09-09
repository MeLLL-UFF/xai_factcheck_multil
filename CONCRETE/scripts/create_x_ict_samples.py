### 
import subprocess

passage_dir = r"G:\GitHub\apps\mestrado\CONCRETE\data\bbc_passages"
out_file = r"G:\GitHub\apps\mestrado\CONCRETE\data\all_ict_samples.jsonl"

for shard_id in range(3):
    command = [
        "python",
        r"G:\GitHub\apps\mestrado\CONCRETE\CORA\mDPR\create_ict_samples.py",
        "--passage_dir", passage_dir,
        "--out_file", out_file,
        "--shard_id", str(shard_id),
        "--num_shards", str(4)
    ]

subprocess.run(command)