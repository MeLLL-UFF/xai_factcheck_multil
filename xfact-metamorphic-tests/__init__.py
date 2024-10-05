from claim_tests import validate_claim_tests
from context_tests import validate_context_tests
from claimant_tests import validate_claimant_tests
from date_tests import validate_date_tests
from utils import gpt_request, maritaca_request, gemini_request, get_tsv_data, create_result_file, remove_label_column, create_grouped_prompt

tsv_file = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\CONCRETE\data\x-fact\zeroshot.tsv"
json_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\xfact-metamorphic-tests\data\zeroshot_tsv.json"
result_path = f"G:\GitHub\apps\mestrado\xai_factcheck_multil\xfact-metamorphic-tests\data\results.json"

data = get_tsv_data(tsv_file,json_path)
test_data = remove_label_column(data)

results = {
    "claim Open AI": gpt_request(create_grouped_prompt(data,validate_claim_tests(test_data))),
    "claim Maritaca AI": maritaca_request(create_grouped_prompt(data,validate_claim_tests(test_data))),
    "claim Gemini AI": gemini_request(create_grouped_prompt(data,validate_claim_tests(test_data))),
    "context Open AI": gpt_request(create_grouped_prompt(data,validate_context_tests(test_data))),
    "context Maritaca AI": maritaca_request(create_grouped_prompt(data,validate_context_tests(test_data))),
    "context Gemini AI": gemini_request(create_grouped_prompt(data,validate_context_tests(test_data))),
    "claimant Open AI": gpt_request(create_grouped_prompt(data,validate_claimant_tests(test_data))),
    "claimant Maritaca AI": maritaca_request(create_grouped_prompt(data,validate_claimant_tests(test_data))),
    "claimant Gemini AI": gemini_request(create_grouped_prompt(data,validate_claimant_tests(test_data))),
    "date Open AI": gpt_request(create_grouped_prompt(data,validate_date_tests(test_data))),
    "date Maritaca AI": maritaca_request(create_grouped_prompt(data,validate_date_tests(test_data))),
    "date Gemini AI": gemini_request(create_grouped_prompt(data,validate_date_tests(test_data))),
}

create_result_file(result_path,results)