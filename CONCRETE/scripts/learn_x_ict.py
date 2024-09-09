import subprocess

path = r"G:\GitHub\apps\mestrado\CONCRETE\CORA\mDPR\run_xict.py"

command = [
    "python -m torch.distributed.launch",
    path,
    "--max_grad_norm", "2.0",
    "--encoder_model_type", "hf_bert",
    "--pretrained_model_cfg", "bert-base-multilingual-uncased",
    "--seed", "12345",
    "--sequence_length", "256",
    "--warmup_steps", "300",
    "--batch_size", "4",
    "--do_lower_case",
    "--train_file", "G:\\GitHub\\apps\\mestrado\\CONCRETE\\data\\all_ict_samples.jsonl_0.tsv",
    "--dev_file", r"G:\GitHub\apps\mestrado\CONCRETE\data\all_ict_samples-trans100.jsonl_3.tsv",
    "--output_dir", "xict_outputs",
    "--checkpoint_file_name", "xICT_biencoder.pt",
    "--learning_rate", "2e-05",
    "--num_train_epochs", "40",
    "--dev_batch_size", "6",
    "--val_av_rank_start_epoch", "30"
]

subprocess.run(command)
