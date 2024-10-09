from claim_tests import change_to_question, remove_non_critical_words, negate_claim,synonym_replacement
from context_tests import remove_all_context, remove_context, add_context, parameter_change_context
from claimant_tests import set_false_claimant, set_true_claimant
from date_tests import remove_all_date, remove_any_date, change_all_date, change_any_date
from utils import gpt_request,process_json, maritaca_request, gemini_request, create_result_file, create_grouped_prompt

result_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\xfact-metamorphic-tests\data\results.json"
json_file_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\CONCRETE\CORA\mDPR\retrieved_docs\zeroshot.xict.json"
data = process_json(json_file_path)

results = {
    "Open AI without test": gpt_request(create_grouped_prompt(data)),
    "Open AI metamorphic tests with date: remove all dates": gpt_request(create_grouped_prompt(remove_all_date(data))),
    "Open AI metamorphic tests with date: remove random date": gpt_request(create_grouped_prompt(remove_any_date(data))),
    "Open AI metamorphic tests with date: change all date": gpt_request(create_grouped_prompt(change_all_date(data))),
    "Open AI metamorphic tests with date: change random dates": gpt_request(create_grouped_prompt(change_any_date(data))),
    "Open AI metamorphic tests with claim: Synonym Replacement": gpt_request(create_grouped_prompt(synonym_replacement(data))),
    "Open AI metamorphic tests with claim: Negated Claim": gpt_request(create_grouped_prompt(negate_claim(data))),
    "Open AI metamorphic tests with claim: Removed Non-Critical Words": gpt_request(create_grouped_prompt(remove_non_critical_words(data))),
    "Open AI metamorphic tests with claim: Changed to Question": gpt_request(create_grouped_prompt(change_to_question(data))),
    "Open AI metamorphic tests with claimant: Adding claimant as a False claimant": gpt_request(create_grouped_prompt(set_false_claimant(data))),
    "Open AI metamorphic tests with claimant: Adding claimant as a True claimant": gpt_request(create_grouped_prompt(set_true_claimant(data))),
    "Open AI metamorphic tests with context: Validating inserting Context with positive Change": gpt_request(create_grouped_prompt(parameter_change_context(data, True))),
    "Open AI metamorphic tests with context: Validating inserting Context with negative Change": gpt_request(create_grouped_prompt(parameter_change_context(data, False))),
    "Open AI metamorphic tests with context: Removing random Context": gpt_request(create_grouped_prompt(remove_context(data))),
    "Open AI metamorphic tests with context: Removing All Context": gpt_request(create_grouped_prompt(remove_all_context(data))),
    "Open AI metamorphic tests with context: Adding Context": gpt_request(create_grouped_prompt(add_context(data))),
    "Maritaca AI without test": maritaca_request(create_grouped_prompt(data)),
    "Maritaca AI metamorphic tests with date: remove all dates": maritaca_request(create_grouped_prompt(remove_all_date(data))),
    "Maritaca AI metamorphic tests with date: remove random date": maritaca_request(create_grouped_prompt(remove_any_date(data))),
    "Maritaca AI metamorphic tests with date: change all date": maritaca_request(create_grouped_prompt(change_all_date(data))),
    "Maritaca AI metamorphic tests with date: change random dates": maritaca_request(create_grouped_prompt(change_any_date(data))),
    "Maritaca AI metamorphic tests with claim: Synonym Replacement": maritaca_request(create_grouped_prompt(synonym_replacement(data))),
    "Maritaca AI metamorphic tests with claim: Negated Claim": maritaca_request(create_grouped_prompt(negate_claim(data))),
    "Maritaca AI metamorphic tests with claim: Removed Non-Critical Words": maritaca_request(create_grouped_prompt(remove_non_critical_words(data))),
    "Maritaca AI metamorphic tests with claim: Changed to Question": maritaca_request(create_grouped_prompt(change_to_question(data))),
    "Maritaca AI metamorphic tests with claimant: Adding claimant as a False claimant": maritaca_request(create_grouped_prompt(set_false_claimant(data))),
    "Maritaca AI metamorphic tests with claimant: Adding claimant as a True claimant": maritaca_request(create_grouped_prompt(set_true_claimant(data))),
    "Maritaca AI metamorphic tests with context: Validating inserting Context with positive Change": maritaca_request(create_grouped_prompt(parameter_change_context(data, True))),
    "Maritaca AI metamorphic tests with context: Validating inserting Context with negative Change": maritaca_request(create_grouped_prompt(parameter_change_context(data, False))),
    "Maritaca AI metamorphic tests with context: Removing random Context": maritaca_request(create_grouped_prompt(remove_context(data))),
    "Maritaca AI metamorphic tests with context: Removing All Context": maritaca_request(create_grouped_prompt(remove_all_context(data))),
    "Maritaca AI metamorphic tests with context: Adding Context": maritaca_request(create_grouped_prompt(add_context(data))),
    "Gemini AI without test": gemini_request(create_grouped_prompt(data)),
    "Gemini AI metamorphic tests with date: remove all dates": gemini_request(create_grouped_prompt(remove_all_date(data))),
    "Gemini AI metamorphic tests with date: remove random date": gemini_request(create_grouped_prompt(remove_any_date(data))),
    "Gemini AI metamorphic tests with date: change all date": gemini_request(create_grouped_prompt(change_all_date(data))),
    "Gemini AI metamorphic tests with date: change random dates": gemini_request(create_grouped_prompt(change_any_date(data))),
    "Gemini AI metamorphic tests with claim: Synonym Replacement": gemini_request(create_grouped_prompt(synonym_replacement(data))),
    "Gemini AI metamorphic tests with claim: Negated Claim": gemini_request(create_grouped_prompt(negate_claim(data))),
    "Gemini AI metamorphic tests with claim: Removed Non-Critical Words": gemini_request(create_grouped_prompt(remove_non_critical_words(data))),
    "Gemini AI metamorphic tests with claim: Changed to Question": gemini_request(create_grouped_prompt(change_to_question(data))),
    "Gemini AI metamorphic tests with claimant: Adding claimant as a False claimant": gemini_request(create_grouped_prompt(set_false_claimant(data))),
    "Gemini AI metamorphic tests with claimant: Adding claimant as a True claimant": gemini_request(create_grouped_prompt(set_true_claimant(data))),
    "Gemini AI metamorphic tests with context: Validating inserting Context with positive Change": gemini_request(create_grouped_prompt(parameter_change_context(data, True))),
    "Gemini AI metamorphic tests with context: Validating inserting Context with negative Change": gemini_request(create_grouped_prompt(parameter_change_context(data, False))),
    "Gemini AI metamorphic tests with context: Removing random Context": gemini_request(create_grouped_prompt(remove_context(data))),
    "Gemini AI metamorphic tests with context: Removing All Context": gemini_request(create_grouped_prompt(remove_all_context(data))),
    "Gemini AI metamorphic tests with context: Adding Context": gemini_request(create_grouped_prompt(add_context(data))),
}

create_result_file(result_path,results)