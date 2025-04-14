import pandas as pd

MUTATIONS_PER_CLAIM = 20

input_path = 'data/processed/labeled_mutated_news_complete.csv'
output_path = 'data/processed/labeled_news_with_ids.csv'

df = pd.read_csv(input_path)

df['news_id'] = (df.index // MUTATIONS_PER_CLAIM) + 1

df_final = df[['Mutated Label', 'Mutation Type', 'news_id']]

df_final.to_csv(output_path, index=False)
print(f"Arquivo salvo com sucesso: {output_path}")
