def remove_claimant(data):
    modified_data = data.copy()
    modified_data['claimant'] = ""

    return modified_data

def set_false_claimant(data):
    modified_data = data.copy()
    modified_data['claimant'] = "Fake News Agency"
    
    return modified_data

def set_true_claimant(data):
    modified_data = data.copy()
    modified_data['claimant'] = "Trusted News Agency"
    
    return modified_data

def validate_claimant_tests(data):
    tests = {
        "Remove claimant": remove_claimant(data),
        "False claimant": set_false_claimant(data),
        "True claimant": set_true_claimant(data),
    }

    return tests