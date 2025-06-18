

import argparse
from . import generate_mutated_table, run_fact_checking


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True,
                        help="Arquivo TSV original (ex: x_fact.tsv)")
    parser.add_argument("--output", type=str, default="results.tsv",
                        help="Arquivo de saída com os resultados")
    parser.add_argument("--model", type=str,
                        help="Nome do modelo (ex: gpt-4, maritaca, gemini)")
    parser.add_argument("--cache", type=str, default=None,
                        help="Diretório para cache das respostas")
    parser.add_argument("--generate_mutations", action="store_true",
                        help="Se definido, gera mutações e salva em TSV")
    parser.add_argument("--mutated_output", type=str,
                        default="xfact-metamorphic-tests\\data\\all_mutations.tsv", help="Arquivo de saída das mutações")
    args = parser.parse_args()

    if args.generate_mutations:
        generate_mutated_table(args.input, args.mutated_output)
    else:
        run_fact_checking(args.input, args.output,
                          args.model, cache_dir=args.cache)
