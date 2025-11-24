"""
Admin dashboard component for viewing assessment history and statistics
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import config

from src.utils.database import (
    get_all_assessments,
    get_statistics,
    delete_assessment,
    export_to_excel,
    is_cloud_environment,
    get_sheet_configured
)


def display_admin_dashboard():
    """Display the admin dashboard with assessment history and statistics"""
    
    st.title("📊 Admin Dashboard")
    st.markdown("View assessment history, statistics, and insights.")
    
    # Check if in cloud environment without Google Sheets configured
    if is_cloud_environment() and not get_sheet_configured():
        st.warning("""
        ℹ️ **Cloud Storage Not Configured**
        
        Assessment data saving is not enabled on this deployment.
        
        **To enable cloud saving:**
        1. Follow the instructions in `SETUP_GOOGLE_SHEET.md`
        2. Create a public Google Sheet
        3. Update `GOOGLE_SHEET_ID` in `src/utils/database.py`
        4. Commit and push changes
        
        **Note:** The app still works perfectly for assessments - only historical 
        data tracking requires this setup.
        """)
        
        st.info("""
        **For local development:**
        - Clone the repository
        - Run the app locally
        - Assessment history will be saved to `data/assessment_history.csv`
        - This dashboard will show all saved assessments
        """)
        return
    
    # Get data
    df = get_all_assessments()
    stats = get_statistics()
    
    if df.empty:
        st.info("No assessment data available yet. Complete an assessment to see statistics here.")
        return
    
    # Display statistics
    st.markdown("---")
    st.subheader("📈 Overview Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Assessments",
            value=stats['total_assessments']
        )
    
    with col2:
        st.metric(
            label="High Risk",
            value=stats['high_risk_count'],
            delta=f"{(stats['high_risk_count']/stats['total_assessments']*100):.1f}%"
        )
    
    with col3:
        st.metric(
            label="Moderate Risk",
            value=stats['moderate_risk_count'],
            delta=f"{(stats['moderate_risk_count']/stats['total_assessments']*100):.1f}%"
        )
    
    with col4:
        st.metric(
            label="Low Risk",
            value=stats['low_risk_count'],
            delta=f"{(stats['low_risk_count']/stats['total_assessments']*100):.1f}%"
        )
    
    # Additional metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Average BMI",
            value=f"{stats['average_bmi']:.1f}"
        )
    
    with col2:
        st.metric(
            label="Average Risk %",
            value=f"{stats['average_risk_percentage']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Gender Split",
            value=f"M: {stats['male_count']} / F: {stats['female_count']}"
        )
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Risk Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk level pie chart
        risk_counts = df['diabetes_risk'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Risk Level Distribution",
            color=risk_counts.index,
            color_discrete_map={
                'Low Risk': '#28a745',
                'Moderate Risk': '#ffc107',
                'High Risk': '#dc3545'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Gender distribution
        gender_counts = df['sex'].value_counts()
        fig_gender = px.bar(
            x=['Female', 'Male'],
            y=[gender_counts.get(0, 0), gender_counts.get(1, 0)],
            title="Gender Distribution",
            labels={'x': 'Gender', 'y': 'Count'},
            color=['Female', 'Male'],
            color_discrete_map={'Female': '#ff6b9d', 'Male': '#4dabf7'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    # BMI distribution
    st.markdown("---")
    st.subheader("📈 BMI Distribution")
    
    fig_bmi = px.histogram(
        df,
        x='bmi',
        nbins=20,
        title="BMI Distribution Across All Assessments",
        labels={'bmi': 'BMI', 'count': 'Number of People'},
        color_discrete_sequence=['#3498db']
    )
    fig_bmi.add_vline(x=25, line_dash="dash", line_color="orange", annotation_text="Overweight")
    fig_bmi.add_vline(x=30, line_dash="dash", line_color="red", annotation_text="Obese")
    st.plotly_chart(fig_bmi, use_container_width=True)
    
    # Risk percentage over time
    st.markdown("---")
    st.subheader("📅 Risk Trends Over Time")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig_time = px.scatter(
        df,
        x='timestamp',
        y='risk_percentage',
        color='diabetes_risk',
        title="Risk Percentage Over Time",
        labels={'timestamp': 'Date', 'risk_percentage': 'Risk %'},
        color_discrete_map={
            'Low Risk': '#28a745',
            'Moderate Risk': '#ffc107',
            'High Risk': '#dc3545'
        }
    )
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Assessment history table
    st.markdown("---")
    st.subheader("📋 Assessment History")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            options=['Low Risk', 'Moderate Risk', 'High Risk'],
            default=['Low Risk', 'Moderate Risk', 'High Risk']
        )
    
    with col2:
        gender_filter = st.multiselect(
            "Filter by Gender",
            options=['Female', 'Male'],
            default=['Female', 'Male']
        )
    
    with col3:
        search_name = st.text_input("Search by Name")
    
    # Apply filters
    filtered_df = df.copy()
    
    if risk_filter:
        filtered_df = filtered_df[filtered_df['diabetes_risk'].isin(risk_filter)]
    
    if gender_filter:
        gender_map = {'Female': 0, 'Male': 1}
        selected_genders = [gender_map[g] for g in gender_filter]
        filtered_df = filtered_df[filtered_df['sex'].isin(selected_genders)]
    
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
    
    # Display table
    display_df = filtered_df[['user_id', 'timestamp', 'name', 'email', 'bmi', 'diabetes_risk', 'risk_percentage']].sort_values('timestamp', ascending=False)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"assessment_history_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Download filtered data
        if not filtered_df.equals(df):
            filtered_csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📄 Download Filtered CSV",
                data=filtered_csv,
                file_name=f"filtered_assessment_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )


def display_recent_assessments():
    """Display recent assessments in a compact format"""
    
    st.subheader("🕐 Recent Assessments")
    
    stats = get_statistics()
    
    if 'recent_assessments' in stats and stats['recent_assessments']:
        for assessment in stats['recent_assessments']:
            with st.expander(f"#{assessment['user_id']} - {assessment['name']} ({assessment['timestamp']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Risk:** {assessment['diabetes_risk']}")
                    st.write(f"**BMI:** {assessment['bmi']:.1f}")
                
                with col2:
                    st.write(f"**Risk %:** {assessment['risk_percentage']:.1f}%")
                    st.write(f"**Gender:** {'Male' if assessment['sex'] == 1 else 'Female'}")
                
                with col3:
                    st.write(f"**Email:** {assessment['email']}")
                    st.write(f"**Prediction:** {'Diabetic' if assessment['prediction'] == 1 else 'Non-Diabetic'}")
    else:
        st.info("No recent assessments available.")
