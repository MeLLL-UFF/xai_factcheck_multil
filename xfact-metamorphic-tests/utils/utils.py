import json
def remove_label_column(data):
    del data.label
    return data

def create_result_file(result_path, results_data):
    with open(result_path, 'w') as json_file:
        json.dump(results_data, json_file, indent=4)