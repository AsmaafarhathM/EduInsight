import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Student Performance Dashboard", 
    page_icon="🎓", 
    layout="wide"
)

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data():
    """Load data from the SQLite database."""
    try:
        conn = sqlite3.connect('data/student_performance.db')
        df = pd.read_sql("SELECT * FROM students", conn)
        conn.close()
        return df
    except sqlite3.OperationalError:
        return None

# --- LOAD DATA ---
df = load_data()

# --- MAIN DASHBOARD INTERFACE ---
st.title("🎓 Student Performance Analytics")
st.markdown("An interactive dashboard to explore factors influencing student test scores.")

if df is None:
    st.error("Database not found! Please run `python3 src/data_processing.py` to generate the SQLite database first.")
else:
    # --- KPIs at the top ---
    st.markdown("### 📊 Metrics Overview")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Total Students", f"{len(df):,}")
    kpi2.metric("Overall Average Score", f"{df['average_score'].mean():.2f}")
    kpi3.metric("Highest Math Score", f"{df['math_score'].max():.0f}")
    
    prep_percentage = (df['test_preparation_course'] == 'completed').mean() * 100
    kpi4.metric("Completed Test Prep", f"{prep_percentage:.1f}%")

    st.markdown("---")

    # --- ROW 1: General Distribution & Demographics ---
    st.markdown("### 1. Score Distributions & Demographics")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Overall Average Score Distribution**")
        fig_dist = px.histogram(df, x="average_score", nbins=20, 
                                marginal="box", color_discrete_sequence=['skyblue'])
        fig_dist.update_layout(xaxis_title="Average Score", yaxis_title="Count")
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        st.write("**Performance Breakdown by Gender**")
        fig_gender = px.box(df, x="gender", y="average_score", color="gender", 
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_gender.update_layout(xaxis_title="Gender", yaxis_title="Average Score")
        st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    # --- ROW 2: Socioeconomics & Preparation ---
    st.markdown("### 2. Impact of Preparation & Socioeconomics")
    col3, col4 = st.columns(2)

    with col3:
        st.write("**Impact of Test Preparation Course**")
        prep_avg = df.groupby('test_preparation_course', as_index=False)['average_score'].mean()
        fig_prep = px.bar(prep_avg, x="test_preparation_course", y="average_score", 
                          color="test_preparation_course", text_auto='.2f',
                          color_discrete_sequence=px.colors.qualitative.Set2)
        fig_prep.update_layout(xaxis_title="Test Preparation Course", yaxis_title="Average Overall Score")
        st.plotly_chart(fig_prep, use_container_width=True)
        
    with col4:
        st.write("**Impact of Lunch Type (Socioeconomic Factor)**")
        lunch_avg = df.groupby('lunch_type', as_index=False)['average_score'].mean()
        fig_lunch = px.bar(lunch_avg, x="lunch_type", y="average_score",
                           color="lunch_type", text_auto='.2f',
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_lunch.update_layout(xaxis_title="Lunch Type", yaxis_title="Average Overall Score")
        st.plotly_chart(fig_lunch, use_container_width=True)

    st.markdown("---")
    
    # --- ROW 3: Interactive Filter ---
    st.markdown("### 3. Subject Score Explorer")
    st.markdown("Select a specific subject to see how scores vary based on parental education.")
    
    subject = st.selectbox("Select Subject:", ["math_score", "reading_score", "writing_score"])
    
    fig_edu = px.violin(df, x="parental_education", y=subject, color="parental_education",
                        box=True, points="all", log_y=False)
    fig_edu.update_layout(xaxis_title="Parental Education Background", 
                          yaxis_title=f"{subject.replace('_', ' ').title()}")
    st.plotly_chart(fig_edu, use_container_width=True)

    # --- Raw Data Expander
    with st.expander("View Raw Data Snippet"):
        st.dataframe(df.head(100))
