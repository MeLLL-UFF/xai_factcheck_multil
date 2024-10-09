import json

import re
import random
from datetime import datetime, timedelta

def remove_label_column(data):
    del data.label
    return data    

def create_result_file(result_path, results_data):
    with open(result_path, 'w') as json_file:
        json.dump(results_data, json_file, indent=4)

def process_json(data):
    processed_data = data.copy()
    
    # Itera sobre cada item no array 'ctxs'
    for ctx in processed_data.get('ctxs', []):
        if 'doc_id' in ctx:
            del ctx['doc_id']
        if 'id' in ctx:
            del ctx['id']
    
    return processed_data

def create_grouped_prompt(data):
    prompt = f"""
    Check the following claim and classifies its class according to one of the following:
    - "true"
    - "mostly true"
    - "partly true/misleading"
    - "complicated/hard to categorise"
    - "other"
    - "mostly false"
    - "false"
    Claim:
    {data}

    return only the class.
    """
    return prompt

def random_date(start_year=1900, end_year=2024):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime("%d/%m/%Y")

def replace_dates(text):
    date_patterns = [
        r"\b(\d{2}/\d{2}/\d{4})\b",  # dd/mm/yyyy
        r"\b(\d{2}-\d{2}-\d{4})\b",  # dd-mm-yyyy
        r"\b(\d{4}-\d{2}-\d{2})\b",  # yyyy-mm-dd
        r"\b(\d{2}/\d{2}/\d{2})\b",  # mm/dd/yyyy
        r"\b([A-Za-z]+ \d{1,2}, \d{4})\b",  # Month dd, yyyy (ex: January 1, 2020)
        r"\b(\d{1,2} [A-Za-z]+ \d{4})\b"  # dd Month yyyy (ex: 1 January 2020)
    ]
    
    for pattern in date_patterns:
        text = re.sub(pattern, lambda match: random_date(), text)
    
    return text

def remove_dates(text):
    date_patterns = [
        r"\b(\d{2}/\d{2}/\d{4})\b",  # dd/mm/yyyy
        r"\b(\d{2}-\d{2}-\d{4})\b",  # dd-mm-yyyy
        r"\b(\d{4}-\d{2}-\d{2})\b",  # yyyy-mm-dd
        r"\b(\d{2}/\d{2}/\d{2})\b",  # mm/dd/yyyy
        r"\b([A-Za-z]+ \d{1,2}, \d{4})\b",  # Month dd, yyyy (ex: January 1, 2020)
        r"\b(\d{1,2} [A-Za-z]+ \d{4})\b"  # dd Month yyyy (ex: 1 January 2020)
    ]
    
    for pattern in date_patterns:
        text = re.sub(pattern, "", text)
    
    return text