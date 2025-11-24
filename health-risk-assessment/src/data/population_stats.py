"""
Population statistics for diabetes risk comparison

These statistics are approximate averages based on health survey data.
They are used to provide context for user's health metrics.
"""

# Population averages for diabetic individuals
DIABETIC_POPULATION = {
    'BMI': 31.2,
    'GenHlth': 3.2,  # 1=Excellent, 5=Poor
    'MentHlth': 5.2,  # Days of poor mental health in past 30 days
    'PhysHlth': 7.8,  # Days of physical illness/injury in past 30 days
    'Age': 9.5,  # Age category (higher = older)
    'HighBP': 0.68,  # 68% have high blood pressure
    'HighChol': 0.58,  # 58% have high cholesterol
    'Smoker': 0.45,  # 45% are smokers
    'PhysActivity': 0.52,  # 52% are physically active
    'Fruits': 0.58,  # 58% consume fruits daily
    'Veggies': 0.72,  # 72% consume vegetables daily
    'HvyAlcoholConsump': 0.08,  # 8% heavy alcohol consumption
    'Stroke': 0.12,  # 12% have had stroke
    'HeartDiseaseorAttack': 0.18,  # 18% have heart disease
    'DiffWalk': 0.28  # 28% have difficulty walking
}

# Population averages for non-diabetic individuals
NON_DIABETIC_POPULATION = {
    'BMI': 27.8,
    'GenHlth': 2.4,  # 1=Excellent, 5=Poor
    'MentHlth': 2.8,  # Days of poor mental health in past 30 days
    'PhysHlth': 3.5,  # Days of physical illness/injury in past 30 days
    'Age': 7.2,  # Age category (higher = older)
    'HighBP': 0.32,  # 32% have high blood pressure
    'HighChol': 0.35,  # 35% have high cholesterol
    'Smoker': 0.38,  # 38% are smokers
    'PhysActivity': 0.72,  # 72% are physically active
    'Fruits': 0.68,  # 68% consume fruits daily
    'Veggies': 0.78,  # 78% consume vegetables daily
    'HvyAlcoholConsump': 0.05,  # 5% heavy alcohol consumption
    'Stroke': 0.03,  # 3% have had stroke
    'HeartDiseaseorAttack': 0.06,  # 6% have heart disease
    'DiffWalk': 0.12  # 12% have difficulty walking
}

# Healthy target ranges
HEALTHY_RANGES = {
    'BMI': {
        'min': 18.5,
        'max': 24.9,
        'description': 'Normal weight'
    },
    'GenHlth': {
        'target': 1,
        'description': 'Excellent health'
    },
    'MentHlth': {
        'target': 0,
        'threshold': 10,
        'description': 'Less than 10 days of poor mental health per month'
    },
    'PhysHlth': {
        'target': 0,
        'threshold': 10,
        'description': 'Less than 10 days of physical illness per month'
    },
    'HighBP': {
        'target': 0,
        'description': 'No high blood pressure'
    },
    'HighChol': {
        'target': 0,
        'description': 'No high cholesterol'
    },
    'Smoker': {
        'target': 0,
        'description': 'Non-smoker'
    },
    'PhysActivity': {
        'target': 1,
        'description': 'Regular physical activity'
    },
    'Fruits': {
        'target': 1,
        'description': 'Daily fruit consumption'
    },
    'Veggies': {
        'target': 1,
        'description': 'Daily vegetable consumption'
    },
    'HvyAlcoholConsump': {
        'target': 0,
        'description': 'Moderate or no alcohol consumption'
    }
}

# Risk factor descriptions
RISK_FACTOR_INFO = {
    'HighBP': {
        'name': 'High Blood Pressure',
        'impact': 'Major risk factor for diabetes and cardiovascular disease',
        'action': 'Monitor blood pressure, reduce sodium, exercise regularly, take prescribed medications'
    },
    'HighChol': {
        'name': 'High Cholesterol',
        'impact': 'Associated with insulin resistance and heart disease',
        'action': 'Eat heart-healthy diet, exercise, maintain healthy weight, consider statins if prescribed'
    },
    'BMI': {
        'name': 'Body Mass Index',
        'impact': 'Obesity (BMI ≥30) significantly increases diabetes risk',
        'action': 'Aim for 5-10% weight loss through diet and exercise'
    },
    'Smoker': {
        'name': 'Smoking',
        'impact': 'Increases insulin resistance and inflammation',
        'action': 'Quit smoking using cessation programs, medications, or support groups'
    },
    'PhysActivity': {
        'name': 'Physical Activity',
        'impact': 'Improves insulin sensitivity and glucose metabolism',
        'action': 'Aim for 150 minutes of moderate activity per week'
    },
    'GenHlth': {
        'name': 'General Health',
        'impact': 'Poor health often indicates metabolic dysfunction',
        'action': 'Address underlying health issues with healthcare provider'
    },
    'Age': {
        'name': 'Age',
        'impact': 'Diabetes risk increases with age',
        'action': 'Focus on healthy aging through diet, exercise, and regular screenings'
    }
}

# Preventive measures by risk factor
PREVENTIVE_MEASURES = {
    'HighBP': [
        'Reduce sodium intake to less than 2,300mg per day',
        'Exercise for 30 minutes most days',
        'Maintain healthy weight',
        'Limit alcohol consumption',
        'Manage stress',
        'Take prescribed blood pressure medications'
    ],
    'HighChol': [
        'Reduce saturated fat and trans fat intake',
        'Increase fiber consumption',
        'Exercise regularly',
        'Maintain healthy weight',
        'Consider plant sterols and stanols',
        'Take prescribed cholesterol medications if needed'
    ],
    'Obesity': [
        'Set realistic weight loss goal (5-10% of body weight)',
        'Reduce calorie intake by 500-750 calories per day',
        'Increase physical activity',
        'Track food intake with a journal or app',
        'Get adequate sleep',
        'Address emotional eating patterns'
    ],
    'Smoking': [
        'Set a quit date',
        'Use nicotine replacement therapy or medications',
        'Join a quit-smoking program',
        'Identify and avoid triggers',
        'Seek support from friends and family',
        'Consider counseling or support groups'
    ],
    'Inactivity': [
        'Start with 10 minutes of activity and gradually increase',
        'Choose activities you enjoy',
        'Schedule exercise like an appointment',
        'Find an exercise buddy for accountability',
        'Break up sitting time with movement breaks',
        'Use a fitness tracker to monitor progress'
    ]
}


def get_comparison_text(feature, user_value, diabetic_avg, non_diabetic_avg):
    """
    Generate comparison text for a feature
    
    Args:
        feature: Feature name
        user_value: User's value
        diabetic_avg: Diabetic population average
        non_diabetic_avg: Non-diabetic population average
    
    Returns:
        str: Comparison text
    """
    if user_value > diabetic_avg:
        return f"Your {feature} is higher than both diabetic and non-diabetic population averages."
    elif user_value > non_diabetic_avg:
        return f"Your {feature} is higher than the non-diabetic average but similar to or lower than the diabetic average."
    else:
        return f"Your {feature} is within the healthy range, similar to the non-diabetic population average."


def get_risk_category(bmi):
    """
    Categorize BMI into risk levels
    
    Args:
        bmi: Body Mass Index value
    
    Returns:
        tuple: (category, description, color)
    """
    if bmi < 18.5:
        return ("Underweight", "May indicate nutritional deficiency", "blue")
    elif bmi < 25:
        return ("Normal Weight", "Healthy weight range", "green")
    elif bmi < 30:
        return ("Overweight", "Increased health risks", "yellow")
    elif bmi < 35:
        return ("Obese Class I", "Moderate health risks", "orange")
    elif bmi < 40:
        return ("Obese Class II", "High health risks", "red")
    else:
        return ("Obese Class III", "Very high health risks", "darkred")
