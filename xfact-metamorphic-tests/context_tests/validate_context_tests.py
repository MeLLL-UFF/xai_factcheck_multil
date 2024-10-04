import random
from utils import translate_back_to_original,translate_claim

def add_context(data, claim):
    modified_data = data.copy()
    new_evidence = translate_back_to_original(translate_claim(claim) + " Esta informação é importante.", 'auto')
    modified_data["evidences"].append(new_evidence)
    return modified_data

def remove_context(data):
    modified_data = data.copy()
    modified_data["evidences"].clear()
    return modified_data

def alter_context(evidence_list, original_lang, is_positive):
    info_type = "verdadeira" if is_positive else "falsa"
    new_evidence = f"Considere como uma evidencia ${info_type}."
    translated_evidence = translate_back_to_original(new_evidence, original_lang)
    evidence_list.insert(random.randint(0, len(evidence_list)), translated_evidence)
    return evidence_list

def parameter_change_context(data, is_positive_evidence):
    modified_data = data.copy()
    altered_evidences_change = alter_context(data["evidences"].copy(), data["language"], is_positive=is_positive_evidence)
    modified_data["evidences"]=altered_evidences_change
    #altered_claim_data_change = data[(data['claim'] == original_claim) & (data['evidences'] == altered_evidences_change)]
    #return (not altered_claim_data_change.empty)
    return modified_data

def validate_context_tests(data, original_claim):
    tests = {
        "Validate Context with positive Change": parameter_change_context(data["evidences"], original_claim, True),
        "Validate Context with negative Change": parameter_change_context(data["evidences"], original_claim, False),
        "Removing Context": remove_context(original_claim),
        "Adding Context": add_context(original_claim),
    }

    return tests
