import pandas as pd
from constants import MONOLINGUAL_LANGUAGES
import charamel
import io
import re

def clean_text(text: str):
    clean_text= text.replace(' ', ' ').replace('"',"'")
    clean_text= clean_text.replace('...','').strip()
    cleaned = re.sub(r'<[^>]+>', '', clean_text)
    cleaned = re.sub(r'http\S+', '_URL_', cleaned)
    fields = cleaned.split('\t')
    
    if len(fields) > 17:
        excess = len(fields) - 17
        combined_field = ' '.join(fields[3:3+excess+1])
        fields = fields[:3] + [combined_field] + fields[3+excess+1:]
    elif len(fields) < 17:
        fields += [''] * (17 - len(fields))

    return '\t'.join(fields) 

def process_dataframe(file_name, encoding):
    try:
        with open(file_name, 'rb') as file:
            content = []
            for line in file.readlines():
                content.append(clean_text(line.decode(encoding=encoding)))
        buffer = io.StringIO("\n".join(content))

        df = pd.read_csv(buffer, 
                delimiter='\t',
                encoding=encoding,
                )
        return df
    except Exception as e:
        print(f"Error in processing dataframe: {e}")
        return None

def read_data(file_name, args=None, is_train_dev=False):
    with open(file_name, 'rb') as file:
        detector = charamel.Detector()
        encoding = detector.detect(file.read())
        file.close()

    try:
        df = process_dataframe(file_name, encoding.value)
    
    except  Exception as e:
        print(f"Error: {e}")
        raise

    return df, encoding.value
