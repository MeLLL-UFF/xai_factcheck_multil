import json
import pandas as pd
from tqdm import tqdm

from .utils import create_grouped_prompt, load_input_tsv, query_model, save_prompts_by_news
from .mutations import ALL_MRs, apply_mr


def generate_mutated_table(input_tsv: str, output_tsv: str):
    """
    Aplica todas as metamorphic relations em cada linha e gera um TSV expandido com os resultados.
    """
    df_original = pd.read_csv(input_tsv, sep="\t")
    all_mutated_rows = []

    for index, row in tqdm(df_original.iterrows(), total=len(df_original), desc="Gerando mutações"):

        original_fields = row.to_dict()
        original_fields["original_index"] = index
        original_fields["applied_mr"] = "original"
        all_mutated_rows.append(original_fields)

        for mr in ALL_MRs:
            mutated_fields = apply_mr(row.to_dict(), mr)
            mutated_fields["original_index"] = index
            mutated_fields["applied_mr"] = mr
            all_mutated_rows.append(mutated_fields)

    df_mutated = pd.DataFrame(all_mutated_rows)
    df_mutated.to_csv(output_tsv, sep="\t", index=False)
    print(f"Tabela de mutações salva em: {output_tsv}")

    save_prompts_by_news(
        df_mutated, base_folder='xfact-metamorphic-tests\\data')


def run_fact_checking(input_path, output_path, model, cache_dir=None):
    data = load_input_tsv(input_path)

    responses = []
    for idx, instance in tqdm(data.iterrows(), total=len(data), desc="Executando queries"):
        prompt = create_grouped_prompt(instance)
        response = query_model(
            model, prompt, cache_dir=cache_dir, metadata=instance)

        result = {
            "original_index": instance.get("original_index", idx),
            "applied_mr": instance.get("applied_mr", "original"),
            "prompt": prompt,
            "model_response": json.dumps(response, ensure_ascii=False)
        }

        responses.append(result)

    df_out = pd.DataFrame(responses)
    df_out.to_csv(output_path, sep="\t", index=False)
    print(f"Resultados salvos em: {output_path}")
