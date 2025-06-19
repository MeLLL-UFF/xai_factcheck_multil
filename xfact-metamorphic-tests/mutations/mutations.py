
from ..date_tests import change_random_evidence_date, change_one_evidence_date, remove_evidence_dates, remove_one_evidence_date, change_claim_date, change_review_date, remove_claim_date, remove_review_date
from ..context_tests import remove_partial_context, remove_all_context, insert_contradictory_evidence, insert_supporting_evidence
from ..claim_tests import synonym_replacement, negate_claim, remove_non_critical_words, change_to_question, sentiment_shift
from ..claimant_tests import set_false_claimant, set_true_claimant, remove_claimant

ALL_MRs = [
    "synonym_replacement",
    "negate_claim",
    "remove_non_critical_words",
    "change_to_question",
    "set_false_claimant",
    "set_true_claimant",
    "remove_claimant",
    "insert_supporting_evidence",
    "insert_contradictory_evidence",
    "remove_partial_context",
    "remove_all_context",
    "change_review_date",
    "change_claim_date",
    "remove_review_date",
    "remove_claim_date",
    "change_random_evidence_date",
    "change_one_evidence_date",
    "remove_evidence_dates",
    "remove_one_evidence_date",
    "sentiment_shift",
]


def apply_mr(instance: dict, mr: str) -> dict:
    if mr == "synonym_replacement":
        return synonym_replacement(instance)
    elif mr == "sentiment_shift":
        return sentiment_shift(instance)
    elif mr == "negate_claim":
        return negate_claim(instance)
    elif mr == "remove_non_critical_words":
        return remove_non_critical_words(instance)
    elif mr == "change_to_question":
        return change_to_question(instance)
    elif mr == "set_false_claimant":
        return set_false_claimant(instance)
    elif mr == "set_true_claimant":
        return set_true_claimant(instance)
    elif mr == "remove_claimant":
        return remove_claimant(instance)
    elif mr == "insert_supporting_evidence":
        return insert_supporting_evidence(instance)
    elif mr == "insert_contradictory_evidence":
        return insert_contradictory_evidence(instance)
    elif mr == "remove_partial_context":
        return remove_partial_context(instance)
    elif mr == "remove_all_context":
        return remove_all_context(instance)
    elif mr == "change_review_date":
        return change_review_date(instance)
    elif mr == "change_claim_date":
        return change_claim_date(instance)
    elif mr == "remove_review_date":
        return remove_review_date(instance)
    elif mr == "remove_claim_date":
        return remove_claim_date(instance)
    elif mr == "change_random_evidence_date":
        return change_random_evidence_date(instance)
    elif mr == "change_one_evidence_date":
        return change_one_evidence_date(instance)
    elif mr == "remove_evidence_dates":
        return remove_evidence_dates(instance)
    elif mr == "remove_one_evidence_date":
        return remove_one_evidence_date(instance)
    else:
        raise ValueError(f"Unknown metamorphic relation: {mr}")


def process_single_mutation(row_dict, mr):
    mutated_fields = apply_mr(row_dict, mr)
    return mutated_fields
