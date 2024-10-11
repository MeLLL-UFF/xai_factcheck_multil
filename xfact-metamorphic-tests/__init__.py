import random

from claim_tests import change_to_question, remove_non_critical_words, negate_claim,synonym_replacement
from context_tests import remove_all_context, remove_context, add_context, parameter_change_context
from claimant_tests import set_false_claimant, set_true_claimant
from date_tests import remove_all_date, remove_any_date, change_all_date, change_any_date
from utils import gpt_request,process_json, maritaca_request, gemini_request, create_result_file, create_grouped_prompt

result_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\xfact-metamorphic-tests\data\results.json"
json_file_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\CONCRETE\CORA\mDPR\retrieved_docs\zeroshot.xict.json"
data = process_json(json_file_path)

num_samples = min(200, len(data))
random_data_samples = random.sample(data, num_samples)
all_results = {}

for i, sample in enumerate(random_data_samples):
    results = {
    "Current data to test":sample,
    "Open AI without test": gpt_request(create_grouped_prompt(sample)),
    "Open AI metamorphic tests with date: remove all dates": gpt_request(create_grouped_prompt(remove_all_date(sample))),
    "Open AI metamorphic tests with date: remove random date": gpt_request(create_grouped_prompt(remove_any_date(sample))),
    "Open AI metamorphic tests with date: change all date": gpt_request(create_grouped_prompt(change_all_date(sample))),
    "Open AI metamorphic tests with date: change random dates": gpt_request(create_grouped_prompt(change_any_date(sample))),
    "Open AI metamorphic tests with claim: Synonym Replacement": gpt_request(create_grouped_prompt(synonym_replacement(sample))),
    "Open AI metamorphic tests with claim: Negated Claim": gpt_request(create_grouped_prompt(negate_claim(sample))),
    "Open AI metamorphic tests with claim: Removed Non-Critical Words": gpt_request(create_grouped_prompt(remove_non_critical_words(sample))),
    "Open AI metamorphic tests with claim: Changed to Question": gpt_request(create_grouped_prompt(change_to_question(sample))),
    "Open AI metamorphic tests with claimant: Adding claimant as a False claimant": gpt_request(create_grouped_prompt(set_false_claimant(sample))),
    "Open AI metamorphic tests with claimant: Adding claimant as a True claimant": gpt_request(create_grouped_prompt(set_true_claimant(sample))),
    "Open AI metamorphic tests with context: Validating inserting Context with positive Change": gpt_request(create_grouped_prompt(parameter_change_context(sample, True))),
    "Open AI metamorphic tests with context: Validating inserting Context with negative Change": gpt_request(create_grouped_prompt(parameter_change_context(sample, False))),
    "Open AI metamorphic tests with context: Removing random Context": gpt_request(create_grouped_prompt(remove_context(sample))),
    "Open AI metamorphic tests with context: Removing All Context": gpt_request(create_grouped_prompt(remove_all_context(sample))),
    "Open AI metamorphic tests with context: Adding Context": gpt_request(create_grouped_prompt(add_context(sample))),
    "Maritaca AI without test": maritaca_request(create_grouped_prompt(sample)),
    "Maritaca AI metamorphic tests with date: remove all dates": maritaca_request(create_grouped_prompt(remove_all_date(sample))),
    "Maritaca AI metamorphic tests with date: remove random date": maritaca_request(create_grouped_prompt(remove_any_date(sample))),
    "Maritaca AI metamorphic tests with date: change all date": maritaca_request(create_grouped_prompt(change_all_date(sample))),
    "Maritaca AI metamorphic tests with date: change random dates": maritaca_request(create_grouped_prompt(change_any_date(sample))),
    "Maritaca AI metamorphic tests with claim: Synonym Replacement": maritaca_request(create_grouped_prompt(synonym_replacement(sample))),
    "Maritaca AI metamorphic tests with claim: Negated Claim": maritaca_request(create_grouped_prompt(negate_claim(sample))),
    "Maritaca AI metamorphic tests with claim: Removed Non-Critical Words": maritaca_request(create_grouped_prompt(remove_non_critical_words(sample))),
    "Maritaca AI metamorphic tests with claim: Changed to Question": maritaca_request(create_grouped_prompt(change_to_question(sample))),
    "Maritaca AI metamorphic tests with claimant: Adding claimant as a False claimant": maritaca_request(create_grouped_prompt(set_false_claimant(sample))),
    "Maritaca AI metamorphic tests with claimant: Adding claimant as a True claimant": maritaca_request(create_grouped_prompt(set_true_claimant(sample))),
    "Maritaca AI metamorphic tests with context: Validating inserting Context with positive Change": maritaca_request(create_grouped_prompt(parameter_change_context(sample, True))),
    "Maritaca AI metamorphic tests with context: Validating inserting Context with negative Change": maritaca_request(create_grouped_prompt(parameter_change_context(sample, False))),
    "Maritaca AI metamorphic tests with context: Removing random Context": maritaca_request(create_grouped_prompt(remove_context(sample))),
    "Maritaca AI metamorphic tests with context: Removing All Context": maritaca_request(create_grouped_prompt(remove_all_context(sample))),
    "Maritaca AI metamorphic tests with context: Adding Context": maritaca_request(create_grouped_prompt(add_context(sample))),
    "Gemini AI without test": gemini_request(create_grouped_prompt(sample)),
    "Gemini AI metamorphic tests with date: remove all dates": gemini_request(create_grouped_prompt(remove_all_date(sample))),
    "Gemini AI metamorphic tests with date: remove random date": gemini_request(create_grouped_prompt(remove_any_date(sample))),
    "Gemini AI metamorphic tests with date: change all date": gemini_request(create_grouped_prompt(change_all_date(sample))),
    "Gemini AI metamorphic tests with date: change random dates": gemini_request(create_grouped_prompt(change_any_date(sample))),
    "Gemini AI metamorphic tests with claim: Synonym Replacement": gemini_request(create_grouped_prompt(synonym_replacement(sample))),
    "Gemini AI metamorphic tests with claim: Negated Claim": gemini_request(create_grouped_prompt(negate_claim(sample))),
    "Gemini AI metamorphic tests with claim: Removed Non-Critical Words": gemini_request(create_grouped_prompt(remove_non_critical_words(sample))),
    "Gemini AI metamorphic tests with claim: Changed to Question": gemini_request(create_grouped_prompt(change_to_question(sample))),
    "Gemini AI metamorphic tests with claimant: Adding claimant as a False claimant": gemini_request(create_grouped_prompt(set_false_claimant(sample))),
    "Gemini AI metamorphic tests with claimant: Adding claimant as a True claimant": gemini_request(create_grouped_prompt(set_true_claimant(sample))),
    "Gemini AI metamorphic tests with context: Validating inserting Context with positive Change": gemini_request(create_grouped_prompt(parameter_change_context(sample, True))),
    "Gemini AI metamorphic tests with context: Validating inserting Context with negative Change": gemini_request(create_grouped_prompt(parameter_change_context(sample, False))),
    "Gemini AI metamorphic tests with context: Removing random Context": gemini_request(create_grouped_prompt(remove_context(sample))),
    "Gemini AI metamorphic tests with context: Removing All Context": gemini_request(create_grouped_prompt(remove_all_context(sample))),
    "Gemini AI metamorphic tests with context: Adding Context": gemini_request(create_grouped_prompt(add_context(sample))),
    }
    all_results[f"Sample {i+1}"] = results
    create_result_file(result_path,all_results)