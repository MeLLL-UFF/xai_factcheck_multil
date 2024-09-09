import subprocess

output_dir = "outputs"
batch_size = 2
eval_batch_size = 2
max_epoch = 12
accumulate_step = 32
model_name = "bert-base-multilingual-cased"

command = [
    "python", "train.py",
    "--output_dir", output_dir,
    "--batch_size", str(batch_size),
    "--eval_batch_size", str(eval_batch_size),
    "--max_epoch", str(max_epoch),
    "--accumulate_step", str(accumulate_step),
    "--model_name", model_name
]

try:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    print("Treinamento concluído com sucesso!")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Erro durante o treinamento:")
    print(e.stderr)