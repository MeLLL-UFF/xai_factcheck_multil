import json
def remove_label_column(data):
    del data.label
    return data

def create_result_file(result_path, results_data):
    with open(result_path, 'w') as json_file:
        json.dump(results_data, json_file, indent=4)

def create_grouped_prompt(data, test):
    prompt = f"""
    Check the following data and classifies the label. If there are no evidences, You can let it empty.
    
    Data:
    {data}
    
    Now, considering that you does not see the original data, applies the following tests and return a label according the new data:
    {test}

    Now, creates a scenario considering all the given tests.
    
    Return, foreach test, one of the following label:
    - "true"
    - "mostly true"
    - "partly true/misleading"
    - "complicated/hard to categorise"
    - "other"
    - "mostly false"
    - "false"
    """
    return prompt
