def load_risk_factors(file_path):
    import json
    
    with open(file_path, 'r') as file:
        risk_factors = json.load(file)
    
    return risk_factors

def format_data(data):
    formatted_data = {}
    for key, value in data.items():
        formatted_data[key] = float(value) if isinstance(value, (int, float)) else value
    return formatted_data

def prepare_data_for_analysis(raw_data):
    formatted_data = format_data(raw_data)
    # Additional processing can be added here
    return formatted_data