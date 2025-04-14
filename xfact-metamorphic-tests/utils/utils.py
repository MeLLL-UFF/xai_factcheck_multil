import json

import re
import random
from datetime import datetime, timedelta
import pandas as pd
import os

def remove_label_column(data):
    del data.label
    return data


def create_result_file(result_path, results_data):
    with open(result_path, 'w') as json_file:
        json.dump(results_data, json_file, indent=4)


def process_json(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for ctx in data.get('ctxs', []):
            if 'doc_id' in ctx:
                del ctx['doc_id']
            if 'id' in ctx:
                del ctx['id']
        return data

def create_grouped_prompt(data):
    prompt = f"""
You are an AI model specialized in verifying news
claims based on provided evidence.  

Rules:  
1) Only use the given evidence to assess the claim.  
2) Do not rely on external knowledge.  
3) If evidence is unclear, classify as 
"complicated/hard to categorize".

**Claim:** "{data['claim']}"  
**Claimant:** "{data['claimant']}"  
**Source Website:** "{data['site']}"  
**Claim Date:** "{data['claim_date']}"  
**Review Date:** "{data['review_date']}"

**Available Evidence:**  
- {data['evidence']}  

**Reference Links:**  
- {data['source']}   

**Instructions:**  
1) Analyze the claim and break it into key components.  
2) Compare the claim with the provided evidence.  
3) Determine the veracity of the claim based 
only on the given evidence:  
   - "true"  
   - "mostly true"  
   - "partly true/misleading"  
   - "complicated/hard to categorize"  
   - "other"  
   - "mostly false"  
   - "false"  
4) Justify your answer step-by-step, indicating which 
evidence supports or contradicts the claim.

**Expected Output Format:**
returns a JSON with the following data:
  "claim": "{data['claim']}",
  "veracity": "true/mostly true/partly true/
  misleading/complicated/hard to categorize/other/
  mostly false/false",
  "supporting_evidence": [
      "evidence": "evidence_1",
      "summary": "How this evidence supports or
      contradicts the claim"
  ],
  "analysis": "Step-by-step reasoning for classification"
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
        # Month dd, yyyy (ex: January 1, 2020)
        r"\b([A-Za-z]+ \d{1,2}, \d{4})\b",
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
        # Month dd, yyyy (ex: January 1, 2020)
        r"\b([A-Za-z]+ \d{1,2}, \d{4})\b",
        r"\b(\d{1,2} [A-Za-z]+ \d{4})\b"  # dd Month yyyy (ex: 1 January 2020)
    ]

    for pattern in date_patterns:
        text = re.sub(pattern, "", text)

    return text