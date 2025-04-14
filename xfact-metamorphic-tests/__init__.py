import argparse
import json
import pandas as pd
from tqdm import tqdm

from utils import create_grouped_prompt, load_input_tsv, query_model, ALL_MRs, apply_mr


def generate_mutated_table(input_tsv: str, output_tsv: str):
    """
    Aplica todas as metamorphic relations em cada linha e gera um TSV expandido com os resultados.
    """
    df_original = pd.read_csv(input_tsv, sep="\t")
    all_mutated_rows = []

    for index, row in tqdm(df_original.iterrows(), total=len(df_original), desc="Gerando mutações"):
        for mr in ALL_MRs:
            mutated_row = row.copy()
            mutated_fields = apply_mr(mutated_row.to_dict(), mr)
            mutated_fields["original_index"] = index
            mutated_fields["applied_mr"] = mr
            all_mutated_rows.append(mutated_fields)

    df_mutated = pd.DataFrame(all_mutated_rows)
    df_mutated.to_csv(output_tsv, sep="\t", index=False)
    print(f"Tabela de mutações salva em: {output_tsv}")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True,
                        help="Arquivo TSV original (ex: x_fact.tsv)")
    parser.add_argument("--output", type=str, default="results.tsv",
                        help="Arquivo de saída com os resultados")
    parser.add_argument("--model", type=str, required=True,
                        help="Nome do modelo (ex: gpt-4, maritaca, gemini)")
    parser.add_argument("--cache", type=str, default=None,
                        help="Diretório para cache das respostas")
    parser.add_argument("--generate_mutations", action="store_true",
                        help="Se definido, gera mutações e salva em TSV")
    parser.add_argument("--mutated_output", type=str,
                        default="all_mutations.tsv", help="Arquivo de saída das mutações")
    args = parser.parse_args()

    if args.generate_mutations:
        generate_mutated_table(args.input, args.mutated_output)
    else:
        run_fact_checking(args.input, args.output,
                          args.model, cache_dir=args.cache)
