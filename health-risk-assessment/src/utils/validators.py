def validate_age(age):
    if not isinstance(age, int) or age < 0:
        raise ValueError("Age must be a non-negative integer.")
    return True

def validate_weight(weight):
    if not isinstance(weight, (int, float)) or weight <= 0:
        raise ValueError("Weight must be a positive number.")
    return True

def validate_height(height):
    if not isinstance(height, (int, float)) or height <= 0:
        raise ValueError("Height must be a positive number.")
    return True

def validate_bmi(bmi):
    if not isinstance(bmi, (int, float)) or bmi <= 0:
        raise ValueError("BMI must be a positive number.")
    return True

def validate_input(data):
    validate_age(data.get('age'))
    validate_weight(data.get('weight'))
    validate_height(data.get('height'))
    validate_bmi(data.get('bmi'))
    return True