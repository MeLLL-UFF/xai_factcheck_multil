import pandas as pd

sabia_df = pd.read_csv('data/processed/Cleaned_Sabia_Predictions.csv')
concrete_df = pd.read_csv(
    'data/processed/simulated_predictions_concrete_fixed.csv')
gpt_df = pd.read_csv('data/processed/GPT-4_Simulated_Predictions__Fixed_.csv')
gemini_df = pd.read_csv(
    'data/processed/Simulated_Gemini_Predictions_Corrected.csv')

sabia_df = sabia_df.rename(
    columns={"Predicted Label": "Sabia_predicted_label"})
concrete_df = concrete_df.rename(
    columns={"Predicted Label": "Concrete_predicted_label"})
gpt_df = gpt_df.rename(
    columns={"GPT-4 Predicted Label": "GPT_predicted_label"})
gemini_df = gemini_df.rename(
    columns={"Gemini_Predictions": "Flash_predicted_label"})

sabia_df = sabia_df[['Mutation Type', 'Sabia_predicted_label']]
concrete_df = concrete_df[['Mutation Type', 'Concrete_predicted_label']]
gpt_df = gpt_df[['Mutation Type', 'GPT_predicted_label']]
gemini_df = gemini_df[['Mutation Type', 'Flash_predicted_label']]

all_dfs = [sabia_df.set_index('Mutation Type'),
           concrete_df.set_index('Mutation Type'),
           gpt_df.set_index('Mutation Type'),
           gemini_df.set_index('Mutation Type')]

unified_df = pd.concat(all_dfs, axis=1).reset_index()

output_path = 'data/processed/unified_predictions.csv'
unified_df.to_csv(output_path, index=False)
print(f"Arquivo unificado salvo em: {output_path}")
