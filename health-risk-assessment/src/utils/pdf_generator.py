"""
PDF report generation utilities
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config


def generate_pdf_report(user_inputs, prediction, probability, risk_level, risk_percentage, risk_factors):
    """
    Generate a comprehensive PDF report of the risk assessment
    
    Args:
        user_inputs: Dictionary of user input values
        prediction: Binary prediction (0 or 1)
        probability: Probability array [prob_no_diabetes, prob_diabetes]
        risk_level: String indicating risk level
        risk_percentage: Numeric risk percentage
        risk_factors: List of identified risk factors
        
    Returns:
        BytesIO: PDF file as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    # Title
    elements.append(Paragraph("Diabetes Risk Assessment Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Date
    date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    elements.append(Paragraph(date_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk Assessment Results
    elements.append(Paragraph("Assessment Results", heading_style))
    
    # Risk level with color
    risk_color = config.RISK_COLORS.get(risk_level.split()[0].lower(), '#000000')
    risk_text = f'<font color="{risk_color}"><b>Risk Level: {risk_level}</b></font>'
    elements.append(Paragraph(risk_text, normal_style))
    elements.append(Paragraph(f"<b>Diabetes Probability: {risk_percentage:.1f}%</b>", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Interpretation
    interpretation = get_risk_interpretation_for_pdf(risk_level)
    elements.append(Paragraph(interpretation, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Your Health Profile
    elements.append(Paragraph("Your Health Profile", heading_style))
    
    # Create table with user inputs
    profile_data = [['Health Metric', 'Your Value']]
    
    for feature in config.FEATURE_NAMES:
        label = config.FEATURE_LABELS.get(feature, feature)
        value = format_value_for_pdf(feature, user_inputs.get(feature))
        profile_data.append([label, value])
    
    profile_table = Table(profile_data, colWidths=[4*inch, 2*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')])
    ]))
    
    elements.append(profile_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Key Risk Factors
    if risk_factors and any(rf['is_risk'] for rf in risk_factors):
        elements.append(Paragraph("Key Risk Factors", heading_style))
        
        risk_factor_data = [['Risk Factor', 'Your Value', 'Contribution']]
        
        for rf in risk_factors:
            if rf['is_risk']:
                risk_factor_data.append([
                    rf['label'],
                    rf['value'],
                    f"{rf['contribution']:.1f}%"
                ])
        
        risk_table = Table(risk_factor_data, colWidths=[3*inch, 2*inch, 1*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FADBD8')])
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    elements.append(Paragraph("Recommendations", heading_style))
    elements.append(Paragraph(
        "<b>⚠️ Important:</b> This assessment is for informational purposes only and does not constitute medical advice. "
        "Please consult with a qualified healthcare provider for proper diagnosis and treatment.",
        normal_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    recommendations = get_basic_recommendations(risk_level)
    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", normal_style))
        elements.append(Spacer(1, 0.05*inch))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Disclaimer
    elements.append(Paragraph("Disclaimer", heading_style))
    disclaimer_text = """
    This diabetes risk assessment is based on machine learning models trained on health survey data. 
    It provides an estimate of risk based on the information you provided. This tool is NOT a substitute 
    for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician 
    or other qualified health provider with any questions you may have regarding a medical condition.
    """
    elements.append(Paragraph(disclaimer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def format_value_for_pdf(feature, value):
    """Format feature value for PDF display"""
    from src.utils.feature_importance import format_feature_value
    return format_feature_value(feature, value)


def get_risk_interpretation_for_pdf(risk_level):
    """Get concise risk interpretation for PDF"""
    interpretations = {
        "Low Risk": "Your current health profile suggests a low probability of developing diabetes. Continue maintaining healthy lifestyle habits.",
        "Moderate Risk": "Your health profile indicates moderate risk. Consider lifestyle modifications and consult with a healthcare provider about prevention strategies.",
        "High Risk": "Your health profile suggests elevated risk for diabetes. We strongly recommend scheduling an appointment with a healthcare provider for comprehensive evaluation and guidance."
    }
    return interpretations.get(risk_level, "Unable to determine risk interpretation.")


def get_basic_recommendations(risk_level):
    """Get basic recommendations for PDF"""
    recommendations = {
        "Low Risk": [
            "Maintain a balanced diet rich in vegetables, fruits, and whole grains",
            "Continue regular physical activity (at least 150 minutes per week)",
            "Monitor your health with regular check-ups",
            "Maintain a healthy weight",
            "Avoid smoking and limit alcohol consumption"
        ],
        "Moderate Risk": [
            "Schedule a check-up with your healthcare provider",
            "Improve diet by reducing processed foods and added sugars",
            "Increase physical activity to 30 minutes daily",
            "Work on achieving and maintaining a healthy weight",
            "Monitor blood sugar, blood pressure, and cholesterol regularly",
            "Manage stress through healthy coping strategies"
        ],
        "High Risk": [
            "⚠️ Schedule an immediate appointment with your healthcare provider",
            "Request comprehensive blood work (fasting glucose, HbA1c, lipid panel)",
            "Discuss preventive medication options with your doctor",
            "Work with a registered dietitian for meal planning",
            "Start a supervised exercise program",
            "Monitor blood sugar regularly as directed by your healthcare provider",
            "Consider referral to an endocrinologist for specialized care"
        ]
    }
    return recommendations.get(risk_level, ["Consult with a healthcare provider for personalized recommendations"])
