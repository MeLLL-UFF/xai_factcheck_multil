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