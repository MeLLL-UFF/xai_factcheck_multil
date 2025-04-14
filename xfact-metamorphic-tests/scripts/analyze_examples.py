import pandas as pd

comparison_df = pd.read_csv(
    'data/processed/xfact_mutation_comparison_normalized.csv')
batches_df = pd.read_csv('data/processed/xfact_all_data_with_mutations_v3.csv')

merged_df = comparison_df.merge(
    batches_df[["news_id", "claim"]],
    left_on="id",
    right_on="news_id",
    how="left"
)

mutated = merged_df[merged_df["mutation_type"] != "original"]

# Casos em que todos os modelos acertam
all_correct = mutated[
    (mutated["gpt_label"] == mutated["expected_label"]) &
    (mutated["gemini_label"] == mutated["expected_label"]) &
    (mutated["sabia_label"] == mutated["expected_label"]) &
    (mutated["concrete_label"] == mutated["expected_label"])
]

# Casos em que todos os modelos erram
all_wrong = mutated[
    (mutated["gpt_label"] != mutated["expected_label"]) &
    (mutated["gemini_label"] != mutated["expected_label"]) &
    (mutated["sabia_label"] != mutated["expected_label"]) &
    (mutated["concrete_label"] != mutated["expected_label"])
]

# Amostragem
sample_correct = all_correct.sample(2, random_state=42)[
    ["id", "mutation_type", "expected_label", "claim"]]
sample_wrong = all_wrong.sample(2, random_state=99)[
    ["id", "mutation_type", "expected_label", "claim"]]

# Adicionar o tipo (para diferenciar no output)
sample_correct["type"] = "All models correct"
sample_wrong["type"] = "All models wrong"

# Combinar e salvar
examples = pd.concat([sample_correct, sample_wrong], ignore_index=True)
output_path = "results/mutation_examples_all_models_agreed.csv"
examples.to_csv(output_path, index=False)

print("Exemplos selecionados:")
print(examples)
print(f"\nArquivo salvo em: {output_path}")
