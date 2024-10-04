
# Função para alterar a data de alegação
def change_claim_date(data, new_date):
    modified_data = data.copy()
    modified_data['claimDate'] = new_date
    return modified_data

# Função para remover a data de alegação
def remove_claim_date(data):
    modified_data = data.copy()
    modified_data['claimDate'] = ""
    return modified_data

# Função para alterar a data de revisão
def change_review_date(data, new_date):
    modified_data = data.copy()
    modified_data['reviewDate'] = new_date
    return modified_data

# Função para remover a data de revisão
def remove_review_date(data):
    modified_data = data.copy()
    modified_data['reviewDate'] = ""
    return modified_data

def validate_date_tests(data):
    tests = {
        "Remove review date": remove_review_date(data),
        "Change review date": change_review_date(data),
        "Remove claim date": remove_claim_date(data),
        "Change claim date": change_claim_date(data),
    }

    return tests

