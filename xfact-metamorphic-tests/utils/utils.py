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
**Claim Date:** "{data['claimDate']}"  
**Review Date:** "{data['reviewDate']}"

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
      "evidence": "evidence",
      "summary": "How this evidence supports or
      contradicts the claim"
  ],
  "analysis": "Step-by-step reasoning for classification"
    """
    return prompt


def save_prompts_by_news(dataframe, base_folder='xfact-metamorphic-tests\\data'):
    for original_index, group in dataframe.groupby('original_index'):
        news_folder = os.path.join(base_folder, str(original_index), 'prompts')
        os.makedirs(news_folder, exist_ok=True)
        group = group.reset_index(drop=True)

        for i, row in group.iterrows():
            data = row.to_dict()

            ctxs = []
            for j in range(1, 6):
                ev = data.get(f'evidence_{j}', '')
                if pd.notna(ev) and ev.strip():
                    ctxs.append(ev.strip())
            data['ctxs'] = ctxs

            evidence_text = "\n- ".join(ctxs)
            if evidence_text:
                evidence_text = "- " + evidence_text
            data['evidence'] = evidence_text

            sources = []
            for j in range(1, 6):
                link = data.get(f'link_{j}', '')
                if pd.notna(link) and link.strip():
                    sources.append(link.strip())

            source_text = "\n- ".join(sources)
            if source_text:
                source_text = "- " + source_text
            data['source'] = source_text

            prompt = create_grouped_prompt(data)
            prompt_filename = os.path.join(news_folder, f"{i}.txt")

            with open(prompt_filename, 'w', encoding='utf-8') as f:
                f.write(prompt)

        print(f"Prompts salvos para notícia {original_index} em {news_folder}")


def random_date(start_year=1900, end_year=2025):
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


def row_to_ctxs(row):
    if isinstance(row, dict):
        data = row
    else:
        data = row.to_dict()
    ctxs = []
    for i in range(1, 6):
        col = f"evidence_{i}"
        if pd.notnull(data.get(col, None)) and str(data[col]).strip() != "":
            ctxs.append(str(data[col]))
    data["ctxs"] = ctxs
    return data


def ctxs_to_row(data):
    result = data.copy()
    ctxs = result.get("ctxs", [])
    for i in range(1, 6):
        col = f"evidence_{i}"
        if i-1 < len(ctxs):
            result[col] = ctxs[i-1]
        else:
            result[col] = ""
    if "ctxs" in result:
        del result["ctxs"]
    return result


def save_partial_results(results, filename):
    df = pd.DataFrame(results)
    if os.path.exists(filename):
        df.to_csv(filename, sep='\t', mode='a', header=False, index=False)
    else:
        df.to_csv(filename, sep='\t', index=False)
