import pandas as pd
import json
import random
import os

def get_tsv_data(tsv_file_path, output_json_path):
    if os.path.exists(output_json_path):
        with open('data/output.json', 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            num_total_news = len(data_json)
    else:
        df = pd.read_csv(tsv_file_path, sep='\t')
        df['ctxs'] = df.drop(columns=['id', 'doc_id'])
        data_json = df.to_dict(orient='records')
        num_total_news = len(data_json)

    if num_total_news >= 200:
        selected_news = random.sample(data_json, 100)
    else:
        selected_news = data_json

    return selected_news

def load_input_tsv(path):
    return pd.read_csv(path, sep="\t")
