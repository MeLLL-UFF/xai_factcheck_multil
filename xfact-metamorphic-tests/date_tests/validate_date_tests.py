from utils import replace_dates, remove_dates

def change_any_date(data):
    modified_data = data.copy()
    modified_data['ctxs'][0] = replace_dates(modified_data['ctx'][0])
    return modified_data

def remove_any_date(data):
    modified_data = data.copy()
    modified_data['ctxs'][0] = remove_dates(modified_data['ctx'][0])
    return modified_data

def change_all_date(data):
    modified_data = data.copy()
    modified_data['ctxs'] = [replace_dates(item) for item in modified_data['ctx']]
    return modified_data

def remove_all_date(data):
    modified_data = data.copy()
    modified_data['ctxs'] = [remove_dates(item) for item in modified_data['ctx']]
    return modified_data

def validate_date_tests(data):
    prompt =f"""
        "Remove any date": {remove_any_date(data)},
        "Remove all dates": {remove_all_date(data)},
        "Change any date": {change_any_date(data)},
        "Change all dates": {change_all_date(data)},
    """
    return prompt
