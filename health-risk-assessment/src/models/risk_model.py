def calculate_risk(user_inputs, risk_factors):
    # Example algorithm for risk calculation
    risk_score = 0
    for factor, value in user_inputs.items():
        if factor in risk_factors:
            risk_score += risk_factors[factor] * value
    return risk_score

def assess_risk(user_inputs):
    # Load risk factors from a predefined source
    risk_factors = {
        'age': 0.1,
        'cholesterol': 0.2,
        'blood_pressure': 0.3,
        'smoking': 0.5,
        'diabetes': 0.4
    }
    
    risk_score = calculate_risk(user_inputs, risk_factors)
    
    # Determine risk level based on score
    if risk_score < 1:
        risk_level = 'Low'
    elif risk_score < 3:
        risk_level = 'Moderate'
    else:
        risk_level = 'High'
    
    return risk_level, risk_score