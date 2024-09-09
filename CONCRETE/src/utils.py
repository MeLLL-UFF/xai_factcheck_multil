import pandas as pd
from constants import MONOLINGUAL_LANGUAGES
import charamel
import re

def normalize_quotes(text):
    if isinstance(text, str):
        text = text.replace('“', '"').replace('”', '"')
        text = text.replace('‘', "'").replace('’', "'")
    return text

def clean_text(text):
    if isinstance(text, str):
        text = text.replace(' ', ' ') 
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_dataframe(file_name, encoding):
    try:
        with open(file_name, 'r', encoding=encoding) as file:
            for i, line in enumerate(file):
                if len(line.split('\t')) != 17:
                    print(f"Line {i + 1} has a different number of fields: {line}")
        
        df = pd.read_csv(file_name, sep='\t', quotechar='"', doublequote=True, encoding=encoding, on_bad_lines='warn')
        
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].apply(normalize_quotes)
        
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].apply(clean_text)
        
        return df
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None

def read_data(file_name, args=None, is_train_dev=False):
    with open(file_name, 'rb') as file:
        detector = charamel.Detector()
        encoding = detector.detect(file.read())
        print("encoding data:", encoding.value)
        file.close()

    try:
        df = process_dataframe(file_name,encoding.value)

    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
        raise
    
    if df is None or df.empty:
        raise ValueError("The DataFrame is empty. Check if the file is read correctly.")
    
    num_columns = len(df.columns)
    if not all(len(row) == num_columns for row in df.values):
        raise ValueError("Inconsistent number of columns in the file.")
    
    if args is not None and (args.do_monolingual_eval or args.do_monolingual_retrieval):
        df = df.loc[df.language.isin(MONOLINGUAL_LANGUAGES)]
    
    if args is not None and len(args.training_subset_langs) > 0 and is_train_dev:
        df = df.loc[df.language.isin(args.training_subset_langs)]
    
    return df, encoding.value