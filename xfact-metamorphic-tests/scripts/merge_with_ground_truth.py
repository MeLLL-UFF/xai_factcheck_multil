import pandas as pd

ground_truth_path = 'data/processed/labeled_news_with_ids.csv'
predictions_path = 'data/processed/unified_predictions_with_news_id.csv'
output_path = 'data/processed/final_merged_predictions.csv'

df_gt = pd.read_csv(ground_truth_path)
df_preds = pd.read_csv(predictions_path)

df_gt = df_gt.rename(
    columns={'Mutated Label': 'original_label', 'news_id': 'original_news_id'})
df_preds = df_preds.rename(columns=lambda x: x.strip())

for df in [df_gt, df_preds]:
    if 'mutation type' in map(str.lower, df.columns):
        for col in df.columns:
            if col.lower() == 'mutation type':
                df.rename(columns={col: 'mutation_type'}, inplace=True)
                break

df_final = pd.merge(
    df_gt[['original_news_id', 'mutation_type', 'original_label']],
    df_preds[['News_ID', 'Mutation Type', 'Sabia_predicted_label',
              'Concrete_predicted_label', 'GPT_predicted_label',
              'Flash_predicted_label']].rename(columns={
                  'News_ID': 'original_news_id',
                  'Mutation Type': 'mutation_type'
              }),
    on=['original_news_id', 'mutation_type'],
    how='inner'
)

df_final = df_final.rename(columns={
    'original_label': 'original_label',
    'Sabia_predicted_label': 'sabia_label',
    'Concrete_predicted_label': 'concrete_label',
    'GPT_predicted_label': 'gpt_label',
    'Flash_predicted_label': 'gemini_label'
})

df_final.reset_index(drop=True, inplace=True)
df_final.insert(0, 'id', df_final.index)
df_final = df_final[[
    'id', 'mutation_type', 'gpt_label', 'sabia_label', 'concrete_label',
    'gemini_label', 'original_news_id', 'original_label'
]]

df_final['expected_label'] = df_final['original_label']


df_final.to_csv(output_path, index=False)
