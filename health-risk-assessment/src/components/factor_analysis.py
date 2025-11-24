"""
Feature analysis component for visualizing risk factors
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def display_feature_importance(feature_importance_df):
    """
    Display overall feature importance from the model
    
    Args:
        feature_importance_df: DataFrame with feature importance scores
    """
    if feature_importance_df is None or feature_importance_df.empty:
        st.warning("Feature importance data is not available for this model.")
        return
    
    st.markdown("### 📊 Model Feature Importance")
    st.markdown("These are the factors that most influence diabetes risk predictions in general:")
    
    # Take top 10 features
    top_features = feature_importance_df.head(10)
    
    # Create horizontal bar chart
    fig = px.bar(
        top_features,
        x='Importance',
        y='Feature_Label',
        orientation='h',
        title='Top 10 Most Important Features in Diabetes Risk Prediction',
        labels={'Importance': 'Importance Score', 'Feature_Label': 'Health Factor'},
        color='Importance',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Importance Score",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_user_risk_factors(risk_factors):
    """
    Display personalized risk factors specific to the user
    
    Args:
        risk_factors: List of dictionaries containing user's risk factors
    """
    st.markdown("---")
    st.markdown("### 🎯 Your Personal Risk Factors")
    st.markdown("Based on your inputs, these factors contributed most to your risk assessment:")
    
    if not risk_factors:
        st.info("No specific risk factors identified.")
        return
    
    # Filter to show only risky factors
    risky_factors = [rf for rf in risk_factors if rf['is_risk']]
    protective_factors = [rf for rf in risk_factors if not rf['is_risk']]
    
    # Display risky factors
    if risky_factors:
        st.markdown("#### 🔴 Risk-Increasing Factors")
        
        for rf in risky_factors:
            with st.expander(f"**{rf['label']}**: {rf['value']} (Contribution: {rf['contribution']:.1f}%)"):
                st.markdown(f"""
                **Your Value:** {rf['value']}
                
                **Impact on Risk:** This factor contributes approximately **{rf['contribution']:.1f}%** to the 
                model's risk calculation.
                
                **Why it matters:** {get_factor_explanation(rf['feature'])}
                """)
        
        # Create a chart for risk factors
        risk_df = pd.DataFrame(risky_factors)
        
        fig = go.Figure(go.Bar(
            x=risk_df['contribution'],
            y=risk_df['label'],
            orientation='h',
            marker=dict(
                color=risk_df['contribution'],
                colorscale='Reds',
                showscale=False
            ),
            text=risk_df['contribution'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Your Risk Factor Contributions",
            xaxis_title="Contribution to Risk (%)",
            yaxis_title="",
            height=max(300, len(risky_factors) * 50),
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Display protective factors
    if protective_factors:
        st.markdown("#### 🟢 Protective Factors")
        st.markdown("These healthy habits are helping to lower your risk:")
        
        for rf in protective_factors[:5]:  # Show top 5 protective factors
            st.success(f"✅ **{rf['label']}**: {rf['value']}")


def display_factor_comparison(user_inputs, population_stats):
    """
    Compare user's values to population averages
    
    Args:
        user_inputs: Dictionary of user input values
        population_stats: Dictionary with diabetic and non_diabetic population averages
    """
    st.markdown("---")
    st.markdown("### 📈 How You Compare to Population Averages")
    st.markdown("See how your health metrics compare to diabetic and non-diabetic populations:")
    
    # Select key numeric features for comparison
    comparison_features = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age']
    
    for feature in comparison_features:
        if feature in user_inputs:
            display_single_comparison(
                feature,
                user_inputs[feature],
                population_stats
            )


def display_single_comparison(feature, user_value, population_stats):
    """
    Display comparison for a single feature
    
    Args:
        feature: Feature name
        user_value: User's value for this feature
        population_stats: Population statistics
    """
    feature_label = config.FEATURE_LABELS.get(feature, feature)
    
    # Format the value for display
    if feature == 'BMI':
        formatted_value = f"{user_value:.1f}"
        diabetic_avg = 31.2  # Approximate average
        non_diabetic_avg = 27.8  # Approximate average
    elif feature == 'GenHlth':
        formatted_value = config.GENERAL_HEALTH_LEVELS[int(user_value)]
        diabetic_avg = 3.2
        non_diabetic_avg = 2.4
    elif feature == 'Age':
        formatted_value = config.AGE_CATEGORIES[int(user_value)]
        diabetic_avg = 9.5
        non_diabetic_avg = 7.2
    elif feature in ['MentHlth', 'PhysHlth']:
        formatted_value = f"{int(user_value)} days"
        if feature == 'MentHlth':
            diabetic_avg = 5.2
            non_diabetic_avg = 2.8
        else:
            diabetic_avg = 7.8
            non_diabetic_avg = 3.5
    else:
        formatted_value = str(user_value)
        diabetic_avg = user_value
        non_diabetic_avg = user_value
    
    # Create comparison chart
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"**{feature_label}**")
        st.metric(label="Your Value", value=formatted_value)
    
    with col2:
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            name='Non-Diabetic Avg',
            x=['Population Average'],
            y=[non_diabetic_avg],
            marker_color='lightgreen',
            text=[f"{non_diabetic_avg:.1f}"],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            name='Diabetic Avg',
            x=['Population Average'],
            y=[diabetic_avg],
            marker_color='lightcoral',
            text=[f"{diabetic_avg:.1f}"],
            textposition='auto'
        ))
        
        fig.add_trace(go.Scatter(
            name='Your Value',
            x=['Population Average'],
            y=[user_value],
            mode='markers',
            marker=dict(size=15, color='darkblue', symbol='diamond'),
            text=[formatted_value]
        ))
        
        fig.update_layout(
            barmode='group',
            height=200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis_title=feature_label
        )
        
        st.plotly_chart(fig, use_container_width=True)


def get_factor_explanation(feature):
    """
    Get explanation for why a factor affects diabetes risk
    
    Args:
        feature: Feature name
        
    Returns:
        str: Explanation text
    """
    explanations = {
        'HighBP': "High blood pressure damages blood vessels and makes it harder for your body to use insulin effectively. It's a major risk factor for both diabetes and cardiovascular disease.",
        'HighChol': "High cholesterol is associated with insulin resistance and metabolic syndrome, which increase diabetes risk. Managing cholesterol is important for overall metabolic health.",
        'BMI': "Higher BMI, especially obesity (BMI ≥ 30), significantly increases diabetes risk. Excess body fat, particularly around the abdomen, contributes to insulin resistance.",
        'Smoker': "Smoking increases inflammation and insulin resistance throughout the body. Smokers are 30-40% more likely to develop type 2 diabetes than non-smokers.",
        'Stroke': "Previous stroke indicates cardiovascular complications that often coexist with diabetes. Both conditions share many underlying risk factors.",
        'HeartDiseaseorAttack': "Heart disease and diabetes frequently occur together. They share risk factors like obesity, high blood pressure, and abnormal cholesterol levels.",
        'PhysActivity': "Physical inactivity reduces insulin sensitivity and promotes weight gain. Regular exercise helps your body use insulin more effectively and maintains healthy blood sugar levels.",
        'Fruits': "Fruit consumption is associated with better overall diet quality and provides fiber and nutrients that support metabolic health.",
        'Veggies': "Vegetable intake is linked to better blood sugar control and lower diabetes risk. Vegetables provide fiber, vitamins, and compounds that support metabolic health.",
        'HvyAlcoholConsump': "Heavy alcohol consumption can affect blood sugar regulation, contribute to weight gain, and increase inflammation, all of which elevate diabetes risk.",
        'GenHlth': "Poor general health often reflects underlying metabolic dysfunction and multiple risk factors that contribute to diabetes development.",
        'MentHlth': "Poor mental health can affect lifestyle choices, stress hormones, and inflammation, all of which influence diabetes risk.",
        'PhysHlth': "Physical health problems may limit activity levels and affect metabolism, contributing to increased diabetes risk.",
        'Age': "Diabetes risk increases with age due to decreased insulin sensitivity, reduced physical activity, and accumulation of risk factors over time.",
        'DiffWalk': "Difficulty with mobility often indicates limited physical activity, which is a significant risk factor for diabetes.",
        'NoDocbcCost': "Lack of healthcare access may mean undiagnosed or unmanaged health conditions, delayed preventive care, and increased health risks."
    }
    
    return explanations.get(feature, "This factor contributes to your overall diabetes risk assessment based on population health data.")
