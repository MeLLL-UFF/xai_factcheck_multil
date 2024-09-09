def summarize_model(model):
    for name, param in model.named_parameters():
        print(f"Layer: {name}, Shape: {param.shape}")

import torch

model_path = r'G:\\GitHub\\apps\\mestrado\\CONCRETE\\CORA\\mDPR\\xict_outputs\\xICT_biencoder.pt.37-002.9188'

try:
    checkpoint = torch.load(model_path, map_location='cpu')
    if isinstance(checkpoint, dict) and 'model_dict' in checkpoint:
        checkpoint = checkpoint['model_dict']
        
    
    print("Modelo carregado com sucesso!")
    
    # Exibir as chaves e tamanhos dos parâmetros no OrderedDict
    print("Parâmetros do modelo:")
    for name, param in checkpoint.items():
        print(f"Layer: {name}, Shape: {param.shape if hasattr(param, 'shape') else type(param)}")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")