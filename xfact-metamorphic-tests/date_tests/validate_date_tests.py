from ..utils import replace_dates, remove_dates, row_to_ctxs, ctxs_to_row
import random
import re
import pandas as pd

def change_random_evidence_date(row):
    data = row_to_ctxs(row)
    if data['ctxs']:
        idx = random.randint(0, len(data['ctxs']) - 1)
        data['ctxs'][idx] = replace_dates(data['ctxs'][idx])
    return ctxs_to_row(data)


def change_one_evidence_date(row):
    data = row_to_ctxs(row)
    if not data['ctxs']:
        return ctxs_to_row(data)

    idx = random.randint(0, len(data['ctxs']) - 1)
    text = data['ctxs'][idx]

    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4}|\d{4})\b'
    dates = re.findall(date_pattern, text)

    if dates:
        one_date = random.choice(dates)
        replaced_text = text.replace(one_date, replace_dates(one_date), 1)
        data['ctxs'][idx] = replaced_text

    return ctxs_to_row(data)


def remove_evidence_dates(row):
    data = row_to_ctxs(row)
    data['ctxs'] = [remove_dates(item) for item in data['ctxs']]
    return ctxs_to_row(data)


def remove_one_evidence_date(row):
    data = row_to_ctxs(row)
    if not data['ctxs']:
        return ctxs_to_row(data)

    idx = random.randint(0, len(data['ctxs']) - 1)
    text = data['ctxs'][idx]

    date_pattern = r'\b(\d{1,2}/\d{1,2}/\d{4}|\d{4})\b'
    dates = re.findall(date_pattern, text)

    if dates:
        one_date = random.choice(dates)
        data['ctxs'][idx] = text.replace(one_date, '', 1)

    return ctxs_to_row(data)


def change_claim_date(row):
    row_out = row.copy()
    if 'claimDate' in row_out and pd.notnull(row_out['claimDate']):
        row_out['claimDate'] = replace_dates(row_out['claimDate'])
    return row_out


def change_review_date(row):
    row_out = row.copy()
    if 'reviewDate' in row_out and pd.notnull(row_out['reviewDate']):
        row_out['reviewDate'] = replace_dates(row_out['reviewDate'])
    return row_out


def remove_claim_date(row):
    row_out = row.copy()
    if 'claimDate' in row_out and pd.notnull(row_out['claimDate']):
        row_out['claimDate'] = remove_dates(row_out['claimDate'])
    return row_out


def remove_review_date(row):
    row_out = row.copy()
    if 'reviewDate' in row_out and pd.notnull(row_out['reviewDate']):
        row_out['reviewDate'] = remove_dates(row_out['reviewDate'])
    return row_out
