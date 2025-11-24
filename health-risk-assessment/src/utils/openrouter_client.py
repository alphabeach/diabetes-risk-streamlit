"""
OpenRouter API client for generating personalized health recommendations
"""
import requests
import json
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def generate_recommendations(user_inputs, risk_level, risk_percentage, risk_factors):
    """
    Generate personalized health recommendations using OpenRouter API
    
    Args:
        user_inputs: Dictionary of user input values
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        risk_factors: List of identified risk factors
        
    Returns:
        str: Generated recommendations or error message
    """
    if not config.OPENROUTER_API_KEY:
        return get_default_recommendations(risk_level)
    
    try:
        # Prepare the prompt
        prompt = create_recommendation_prompt(user_inputs, risk_level, risk_percentage, risk_factors)
        
        # API request
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant providing general health guidance. Always remind users to consult healthcare professionals for personalized medical advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            config.OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result['choices'][0]['message']['content']
            return recommendations
        else:
            return get_default_recommendations(risk_level)
            
    except Exception as e:
        print(f"Error generating AI recommendations: {str(e)}")
        return get_default_recommendations(risk_level)


def create_recommendation_prompt(user_inputs, risk_level, risk_percentage, risk_factors):
    """
    Create a detailed prompt for the AI to generate recommendations
    
    Args:
        user_inputs: Dictionary of user input values
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        risk_factors: List of identified risk factors
        
    Returns:
        str: Formatted prompt
    """
    risk_factor_summary = "\n".join([
        f"- {rf['label']}: {rf['value']}" 
        for rf in risk_factors if rf['is_risk']
    ])
    
    prompt = f"""
A person has completed a diabetes risk assessment with the following results:

**Risk Level:** {risk_level} ({risk_percentage:.1f}%)

**Key Risk Factors:**
{risk_factor_summary if risk_factor_summary else "No major risk factors identified"}

**Key Health Metrics:**
- BMI: {user_inputs.get('BMI', 'N/A')}
- Age Category: {config.AGE_CATEGORIES.get(int(user_inputs.get('Age', 7)), 'N/A')}
- General Health: {config.GENERAL_HEALTH_LEVELS.get(int(user_inputs.get('GenHlth', 3)), 'N/A')}
- Physical Activity: {'Yes' if user_inputs.get('PhysActivity', 0) == 1 else 'No'}

Please provide:
1. **3-5 specific, actionable lifestyle recommendations** tailored to their risk factors
2. **Dietary suggestions** if relevant
3. **Exercise recommendations** if appropriate
4. A reminder to consult with healthcare professionals for personalized medical advice

Keep the response concise (250 words max), empathetic, and actionable. Focus on evidence-based recommendations.
"""
    
    return prompt


def get_default_recommendations(risk_level):
    """
    Provide default recommendations when API is unavailable
    
    Args:
        risk_level: String indicating risk level
        
    Returns:
        str: Default recommendations
    """
    recommendations = {
        "Low Risk": """
### 🎯 Maintain Your Healthy Lifestyle

**Continue These Good Habits:**
- Maintain a balanced diet rich in vegetables, fruits, whole grains, and lean proteins
- Stay physically active with at least 150 minutes of moderate exercise per week
- Monitor your weight and keep BMI in healthy range
- Get regular health check-ups and screenings
- Stay hydrated and limit sugary beverages
- Manage stress through relaxation techniques

**Prevention Tips:**
- Continue monitoring your health metrics regularly
- Avoid smoking and limit alcohol consumption
- Get adequate sleep (7-9 hours per night)

⚠️ **Important:** These are general recommendations. Please consult with a healthcare provider for personalized medical advice.
        """,
        
        "Moderate Risk": """
### ⚠️ Take Action to Reduce Your Risk

**Immediate Steps:**
- **Schedule a check-up** with your healthcare provider for comprehensive evaluation
- **Improve your diet** by reducing processed foods, sugar, and refined carbohydrates
- **Increase physical activity** to at least 30 minutes daily, 5 days a week
- **Monitor your blood sugar** levels if recommended by your doctor
- **Manage your weight** if BMI is above healthy range

**Lifestyle Modifications:**
- Choose whole grains over refined grains
- Include more vegetables and fiber in your diet
- Practice portion control
- Reduce stress through mindfulness or meditation
- Quit smoking if applicable
- Limit alcohol consumption

**Regular Monitoring:**
- Get blood sugar tested as recommended
- Check blood pressure regularly
- Monitor cholesterol levels

⚠️ **Important:** Consult with a healthcare provider to develop a personalized prevention plan.
        """,
        
        "High Risk": """
### 🚨 Urgent: Consult a Healthcare Provider

**Immediate Actions Required:**
- **⚠️ Schedule an appointment with your doctor IMMEDIATELY** for proper medical evaluation
- **Request blood work** including fasting glucose, HbA1c, and lipid panel
- **Discuss medication options** if lifestyle changes alone are insufficient
- **Consider a referral to an endocrinologist** for specialized care

**Critical Lifestyle Changes:**
- **Diet:** Work with a registered dietitian to create a meal plan that controls blood sugar
  - Eliminate added sugars and refined carbohydrates
  - Focus on low-glycemic index foods
  - Control portion sizes strictly
  
- **Exercise:** Start with 10-15 minutes daily and gradually increase
  - Walking is an excellent low-impact option
  - Include both aerobic and strength training
  
- **Weight Management:** Even 5-10% weight loss can significantly reduce risk
- **Blood Pressure & Cholesterol:** Manage aggressively under medical supervision
- **Quit Smoking:** Seek support programs if needed

**Monitoring:**
- Check blood sugar regularly as directed by your doctor
- Monitor blood pressure daily if elevated
- Keep a health diary tracking diet, exercise, and symptoms

⚠️ **CRITICAL:** This assessment is NOT a diagnosis. Professional medical evaluation and treatment are essential. Do not delay seeking medical care.
        """
    }
    
    return recommendations.get(risk_level, "Please consult with a healthcare provider for personalized recommendations.")
