def change_claim_date(data, new_date):
    modified_data = data.copy()
    modified_data['claimDate'] = new_date
    return modified_data

def remove_claim_date(data):
    modified_data = data.copy()
    modified_data['claimDate'] = ""
    return modified_data

def change_review_date(data, new_date):
    modified_data = data.copy()
    modified_data['reviewDate'] = new_date
    return modified_data

def remove_review_date(data):
    modified_data = data.copy()
    modified_data['reviewDate'] = ""
    return modified_data

def validate_date_tests(data):
    prompt =f"""
        "Remove review date": {remove_review_date(data)},
        "Change review date": {change_review_date(data)},
        "Remove claim date": {remove_claim_date(data)},
        "Change claim date": {change_claim_date(data)},
        In these tests, there are no need to repeat tests that contradict eachother.
    """
    return prompt
