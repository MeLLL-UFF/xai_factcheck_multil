import subprocess

# Lista dos idiomas
languages = ['en', 'ar', 'fa', 'fr', 'id', 'pt', 'ru']

model_file = 'G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\checkpoints\\xICT_biencoder.pt.37-002.9188'
batch_size = 64
ctx_file_template = 'G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\data\\bbc_passages\\{}'
out_file_template = 'G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\CORA\\mDPR\\embeddings_multilingual\\emb_{}.pkl'

for lang in languages:
    ctx_file = ctx_file_template.format(lang)
    out_file = out_file_template.format(lang)
    command = [
        'python', r"G:\\GitHub\\apps\\mestrado\\xai_factcheck_multil\\CONCRETE\\CORA\\mDPR\\generate_dense_embeddings.py",
        '--model_file', model_file,
        '--batch_size', str(batch_size),
        '--ctx_file', ctx_file,
        '--out_file', out_file
    ]
    
    # Executa o comando
    subprocess.run(command)