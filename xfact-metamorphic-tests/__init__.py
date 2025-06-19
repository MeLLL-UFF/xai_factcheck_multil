import json
import pandas as pd
from tqdm import tqdm
import concurrent.futures
import os
from .utils import create_grouped_prompt, load_input_tsv, query_model, save_prompts_by_news, save_partial_results
from .mutations import ALL_MRs, process_single_mutation


def generate_mutated_table(input_tsv: str, output_tsv: str):
    """
    Aplica todas as metamorphic relations em cada linha e gera um TSV expandido com os resultados.
    """
    df_original = pd.read_csv(input_tsv, sep="\t")
    results = []
    counter = 0

    max_workers = min(12, (os.cpu_count() or 1)+4)

    total_mutations = len(df_original) * (len(ALL_MRs) + 1)
    print(f"Processing {len(df_original)} news")
    print(f"Total Mutations: {total_mutations}")
    print(f"Using {max_workers} workers")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for index, row in df_original.iterrows():
            row_dict = row.to_dict()
            original_fields = row_dict.copy()
            original_fields["original_index"] = index
            original_fields["applied_mr"] = "original"
            results.append(original_fields)
            counter += 1

            for mr in ALL_MRs:
                futures.append(executor.submit(
                    process_single_mutation, row_dict, mr))

        for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Gerando mutações"):
            mutated_fields = f.result()
            results.append(mutated_fields)
            counter += 1

            if counter % 3000 == 0:
                print(f"Salvando progresso com {counter} mutações...")
                save_partial_results(results, output_tsv)
                results.clear()

    if results:
        print(f"Salvando progresso final com {counter} mutações...")
        save_partial_results(results, output_tsv)

    print(f"Tabela de mutações salva em: {output_tsv}")


def generate_prompts(input_tsv):
    base_folder = f'xfact-metamorphic-tests\\data'
    df_mutated = pd.read_csv(input_tsv, sep="\t")
    save_prompts_by_news(df_mutated, base_folder)


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
