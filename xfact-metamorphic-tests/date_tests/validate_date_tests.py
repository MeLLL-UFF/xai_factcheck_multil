from utils import replace_dates, remove_dates
import random
import re

# Replace all dates in one random evidence


def change_random_evidence_date(data):
    modified_data = data.copy()
    if modified_data['ctxs']:
        idx = random.randint(0, len(modified_data['ctxs']) - 1)
        modified_data['ctxs'][idx] = replace_dates(modified_data['ctxs'][idx])
    return modified_data

# Replace only one date in one random evidence


def change_one_evidence_date(data):
    modified_data = data.copy()
    if not modified_data['ctxs']:
        return modified_data

    idx = random.randint(0, len(modified_data['ctxs']) - 1)
    text = modified_data['ctxs'][idx]

    # Regex simplificado para encontrar datas (dd/mm/yyyy ou yyyy)
    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4}|\d{4})\b'
    dates = re.findall(date_pattern, text)

    if dates:
        one_date = random.choice(dates)
        replaced_text = text.replace(one_date, replace_dates(one_date), 1)
        modified_data['ctxs'][idx] = replaced_text

    return modified_data

# Remove all dates from all evidences


def remove_evidence_dates(data):
    modified_data = data.copy()
    modified_data['ctxs'] = [remove_dates(item)
                             for item in modified_data['ctxs']]
    return modified_data

# Remove one date from one random evidence

def remove_one_evidence_date(data):
    modified_data = data.copy()
    if not modified_data['ctxs']:
        return modified_data

    idx = random.randint(0, len(modified_data['ctxs']) - 1)
    text = modified_data['ctxs'][idx]

    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4}|\d{4})\b'
    dates = re.findall(date_pattern, text)

    if dates:
        one_date = random.choice(dates)
        modified_data['ctxs'][idx] = text.replace(one_date, '', 1)

    return modified_data

# Claim/review date replacements


def change_claim_date(data):
    modified_data = data.copy()
    if 'claim_date' in modified_data:
        modified_data['claim_date'] = replace_dates(
            modified_data['claim_date'])
    return modified_data


def change_review_date(data):
    modified_data = data.copy()
    if 'review_date' in modified_data:
        modified_data['review_date'] = replace_dates(
            modified_data['review_date'])
    return modified_data


def remove_claim_date(data):
    modified_data = data.copy()
    if 'claim_date' in modified_data:
        modified_data['claim_date'] = remove_dates(modified_data['claim_date'])
    return modified_data


def remove_review_date(data):
    modified_data = data.copy()
    if 'review_date' in modified_data:
        modified_data['review_date'] = remove_dates(
            modified_data['review_date'])
    return modified_data
