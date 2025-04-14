import pandas as pd

input_path = 'data/processed/xfact_mutation_comparison_with_ground_truth_clean.csv'
output_path = 'data/processed/xfact_mutation_comparison_normalized.csv'

df = pd.read_csv(input_path)

label_mapping = {
    'partly true/misleading': 'partly true',
    'complicated/hard to categorise': 'complicated',
    'complicated/hard to categorize': 'complicated',
    False: 'false'
}

cols_to_normalize = ['expected_label', 'gpt_label',
                     'sabia_label', 'gemini_label', 'concrete_label']

df[cols_to_normalize] = df[cols_to_normalize].replace(label_mapping)

for col in cols_to_normalize:
    df[col] = df[col].astype(str).str.strip()

df.to_csv(output_path, index=False)
print(f"Arquivo normalizado salvo em: {output_path}")
