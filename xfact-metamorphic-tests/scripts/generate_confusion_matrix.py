import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import os

# Caminho de entrada
input_path = 'data/processed/xfact_mutation_comparison_normalized.csv'
output_dir = 'results/confusion_matrices'
os.makedirs(output_dir, exist_ok=True)

# Carregar dados
df = pd.read_csv('data/processed/xfact_mutation_comparison_normalized.csv')

model_labels = {
    'gpt_label': 'GPT-4',
    'gemini_label': 'Gemini',
    'sabia_label': 'Sabia',
    'concrete_label': 'Concrete'
}

label_order = sorted(df['expected_label'].unique())

for column_name, model_name in model_labels.items():
    cm = confusion_matrix(df['expected_label'],
                          df[column_name], labels=label_order)

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=label_order, yticklabels=label_order)

    plt.xlabel('Predicted Label')
    plt.ylabel('Expected Label')
    plt.title(f'Matriz de Confusão - {model_name}')
    plt.tight_layout()

    output_file = os.path.join(
        output_dir, f'{model_name.lower()}_confusion_matrix.png')
    plt.savefig(output_file)
    plt.close()

    print(f"[✔] Matriz de confusão salva: {output_file}")
