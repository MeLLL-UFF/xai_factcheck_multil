import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("../data/xfact_mutation_comparison_with_ground_truth.csv")
df_mutated = df[df['mutation_type'] != 'original'].copy()
df_mutated['expected_label'] = df_mutated['expected_label'].astype(str)

le = LabelEncoder()
le.fit(df_mutated['expected_label'])
results = {}

model_columns = [col for col in df_mutated.columns if col.endswith('_label')]

for model in model_columns:
    filtered = df_mutated[~df_mutated[model].isna()].copy()
    filtered[model] = filtered[model].astype(str)

    y_true = le.transform(filtered['expected_label'])
    y_pred = le.transform(filtered[model])

    results[model] = {
        'Macro-F1': round(f1_score(y_true, y_pred, average='macro'), 4),
        'Macro-Precision': round(precision_score(y_true, y_pred, average='macro', zero_division=0), 4),
        'Macro-Recall': round(recall_score(y_true, y_pred, average='macro', zero_division=0), 4)
    }

results_df = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Model'})
print(results_df)