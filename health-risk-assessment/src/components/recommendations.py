"""
Recommendations component for displaying health recommendations
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def display_recommendations(recommendations_text, risk_level):
    """
    Display personalized health recommendations
    
    Args:
        recommendations_text: AI-generated or default recommendations
        risk_level: String indicating risk level
    """
    st.markdown("---")
    st.markdown("### 💡 Personalized Health Recommendations")
    
    # Add appropriate icon based on risk level
    if risk_level == "High Risk":
        st.error("⚠️ **IMPORTANT:** These recommendations are general guidance. Please consult with a healthcare provider immediately for personalized medical advice.")
    elif risk_level == "Moderate Risk":
        st.warning("⚠️ **Note:** These recommendations are general guidance. Please consult with a healthcare provider for personalized medical advice.")
    else:
        st.info("ℹ️ **Note:** These recommendations are general guidance for maintaining good health.")
    
    st.markdown("---")
    
    # Display recommendations
    st.markdown(recommendations_text)
    
    # Add quick action buttons
    st.markdown("---")
    st.markdown("### 🎯 Quick Action Steps")
    
    if risk_level == "High Risk":
        display_high_risk_actions()
    elif risk_level == "Moderate Risk":
        display_moderate_risk_actions()
    else:
        display_low_risk_actions()


def display_high_risk_actions():
    """Display action items for high-risk users"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🚨 Immediate Actions
        - [ ] Schedule doctor appointment within 1 week
        - [ ] Request blood work (fasting glucose, HbA1c)
        - [ ] Start tracking blood sugar if advised
        - [ ] Review all medications with doctor
        - [ ] Discuss medication options
        """)
    
    with col2:
        st.markdown("""
        #### 📋 Lifestyle Changes to Start Today
        - [ ] Cut out sugary drinks and snacks
        - [ ] Start 10-minute daily walks
        - [ ] Measure portions at meals
        - [ ] Keep a food diary
        - [ ] Check blood pressure daily
        """)
    
    st.error("""
    **🏥 Find Healthcare:**
    - Contact your primary care physician
    - Visit a local community health center
    - Use telehealth services if in-person visits are difficult
    - Ask about diabetes prevention programs in your area
    """)


def display_moderate_risk_actions():
    """Display action items for moderate-risk users"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📅 Within 1 Month
        - [ ] Schedule preventive care appointment
        - [ ] Get baseline blood sugar test
        - [ ] Start exercise routine (3-5 days/week)
        - [ ] Plan healthier meals
        - [ ] Set weight loss goal (if needed)
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 Lifestyle Improvements
        - [ ] Increase vegetable intake
        - [ ] Reduce processed food consumption
        - [ ] Add 30 min daily physical activity
        - [ ] Improve sleep habits (7-9 hours)
        - [ ] Practice stress management
        """)
    
    st.info("""
    **📚 Educational Resources:**
    - Learn about prediabetes prevention
    - Research diabetes prevention programs (DPP)
    - Consult with a registered dietitian
    - Consider joining a fitness class or walking group
    """)


def display_low_risk_actions():
    """Display action items for low-risk users"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### ✅ Maintain Good Habits
        - [ ] Continue regular physical activity
        - [ ] Keep eating balanced meals
        - [ ] Stay hydrated
        - [ ] Get annual health screenings
        - [ ] Monitor weight regularly
        """)
    
    with col2:
        st.markdown("""
        #### 🌟 Optimize Your Health
        - [ ] Try new healthy recipes
        - [ ] Increase workout intensity
        - [ ] Practice mindfulness/meditation
        - [ ] Ensure quality sleep
        - [ ] Stay socially connected
        """)
    
    st.success("""
    **🎉 Keep Up the Great Work!**
    You're doing well! Continue your healthy lifestyle and get regular check-ups to maintain your low risk status.
    """)


def display_lifestyle_tips():
    """Display general lifestyle tips"""
    st.markdown("---")
    st.markdown("### 📚 Evidence-Based Lifestyle Tips")
    
    tabs = st.tabs(["🍎 Nutrition", "🏃 Exercise", "😴 Sleep", "🧘 Stress Management"])
    
    with tabs[0]:
        st.markdown("""
        #### Nutrition Guidelines
        
        **Foods to Emphasize:**
        - Non-starchy vegetables (leafy greens, broccoli, peppers)
        - Whole grains (brown rice, quinoa, oats)
        - Lean proteins (fish, chicken, beans, tofu)
        - Healthy fats (nuts, avocado, olive oil)
        - Fresh fruits in moderation
        
        **Foods to Limit:**
        - Sugary drinks and sodas
        - Refined carbohydrates (white bread, pastries)
        - Processed snacks and fast food
        - High-sugar desserts
        - Excessive alcohol
        
        **Practical Tips:**
        - Use smaller plates for portion control
        - Fill half your plate with vegetables
        - Choose water or unsweetened beverages
        - Read nutrition labels carefully
        - Plan meals in advance
        """)
    
    with tabs[1]:
        st.markdown("""
        #### Exercise Recommendations
        
        **Aerobic Exercise:**
        - Target: 150 minutes per week of moderate activity
        - Examples: Brisk walking, swimming, cycling, dancing
        - Start small and gradually increase
        - Break it into 10-minute sessions if needed
        
        **Strength Training:**
        - Target: 2-3 days per week
        - Examples: Weightlifting, resistance bands, bodyweight exercises
        - Builds muscle and improves insulin sensitivity
        
        **Daily Movement:**
        - Take stairs instead of elevator
        - Park farther from entrances
        - Stand and stretch every hour
        - Walk during phone calls
        - Do household chores actively
        
        **Getting Started:**
        - Start with just 10 minutes daily
        - Choose activities you enjoy
        - Find an exercise buddy
        - Track your progress
        - Celebrate small wins
        """)
    
    with tabs[2]:
        st.markdown("""
        #### Sleep Hygiene
        
        **Importance of Sleep:**
        - Poor sleep affects blood sugar regulation
        - Sleep deprivation increases diabetes risk
        - Target: 7-9 hours per night
        
        **Better Sleep Habits:**
        - Maintain consistent sleep schedule
        - Create dark, cool sleeping environment
        - Limit screen time before bed
        - Avoid caffeine after 2 PM
        - Establish relaxing bedtime routine
        - Exercise regularly (but not close to bedtime)
        - Limit large meals before sleep
        
        **Sleep Disorders:**
        If you experience persistent sleep problems or snoring, 
        consult a healthcare provider about sleep apnea screening.
        """)
    
    with tabs[3]:
        st.markdown("""
        #### Stress Management
        
        **Why It Matters:**
        - Chronic stress raises blood sugar levels
        - Stress hormones affect insulin function
        - Stress can lead to unhealthy coping behaviors
        
        **Stress Reduction Techniques:**
        - **Mindfulness meditation:** 10-15 minutes daily
        - **Deep breathing exercises:** 4-7-8 breathing technique
        - **Physical activity:** Great stress reliever
        - **Social connection:** Spend time with loved ones
        - **Hobbies:** Engage in enjoyable activities
        - **Time in nature:** Walk in parks or natural settings
        - **Professional help:** Therapy or counseling when needed
        
        **Daily Practices:**
        - Start day with positive intentions
        - Practice gratitude journaling
        - Set boundaries with work/technology
        - Take regular breaks throughout day
        - End day with reflection and relaxation
        """)


def display_resources():
    """Display helpful resources and links"""
    st.markdown("---")
    st.markdown("### 🔗 Helpful Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📖 Educational Resources
        - **CDC Diabetes Prevention Program**
          Learn about evidence-based programs
        - **American Diabetes Association**
          Comprehensive diabetes information
        - **National Institute of Diabetes**
          Research and educational materials
        - **Academy of Nutrition and Dietetics**
          Find registered dietitians
        """)
    
    with col2:
        st.markdown("""
        #### 🏥 Getting Help
        - **Find a Doctor:** Use your insurance provider directory
        - **Community Health Centers:** Often offer sliding-scale fees
        - **Diabetes Prevention Programs:** CDC-recognized programs nationwide
        - **Telehealth:** Virtual consultations available
        """)
    
    st.info("""
    **💬 Support Groups:**
    Consider joining diabetes prevention or healthy lifestyle support groups in your community 
    or online. Peer support can be invaluable for making lasting lifestyle changes.
    """)
