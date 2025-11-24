from streamlit import markdown, container

def display_results(risk_prediction, probability_score, recommendations):
    with container():
        markdown("## Risk Assessment Results")
        markdown(f"**Risk Prediction:** {risk_prediction}")
        markdown(f"**Probability Score:** {probability_score:.2f}")
        
        markdown("### Recommendations:")
        for recommendation in recommendations:
            markdown(f"- {recommendation}")