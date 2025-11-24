def calculate_risk(user_inputs):
    # Example risk factors and weights (these should be replaced with actual data)
    risk_factors = {
        'age': 0.1,
        'weight': 0.2,
        'height': -0.1,
        'smoking': 0.3,
        'exercise': -0.2,
        'diet': 0.15
    }

    # Initialize risk score
    risk_score = 0.0

    # Calculate risk based on user inputs
    for factor, weight in risk_factors.items():
        if factor in user_inputs:
            risk_score += user_inputs[factor] * weight

    # Calculate probability score (for example, scale it to a percentage)
    probability_score = min(max(risk_score, 0), 1) * 100

    return risk_score, probability_score

def assess_risk(user_inputs):
    risk_score, probability_score = calculate_risk(user_inputs)
    return {
        'risk_score': risk_score,
        'probability_score': probability_score
    }