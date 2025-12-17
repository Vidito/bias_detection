import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_generation import generate_data
from score_calculation import calculate_scores
from bias_detection import detect_bias
import os

# Page Config
st.set_page_config(page_title="OptiLive: Social Utility Score Audit", layout="wide")

# Title and Intro
st.title("🏙️ OptiLive: Social Utility Score Audit Tool (2030)")
st.markdown("""
**Scenario: Germany 2030 Housing Crisis**
The Department of Housing uses "OptiLive" to assign housing based on a "Social Utility Score".
This tool audits the algorithm for potential bias against protected groups.
""")

# Sidebar
st.sidebar.header("Control Panel")
num_records = st.sidebar.slider("Number of Citizens", 100, 5000, 1000)
seed_val = st.sidebar.number_input("Random Seed", value=42)

if st.sidebar.button("Generate & Score Data"):
    with st.spinner("Generating synthetic citizens..."):
        df = generate_data(num_records)
        df = calculate_scores(df)
        df.to_csv("scored_citizens.csv", index=False)
        st.session_state['data'] = df
        st.success(f"Generated {len(df)} records!")

# Load data if exists
if 'data' not in st.session_state:
    if os.path.exists("scored_citizens.csv"):
        st.session_state['data'] = pd.read_csv("scored_citizens.csv")
    else:
        st.warning("Please generate data to start.")

if 'data' in st.session_state:
    df = st.session_state['data']
    
    # Tabs
    tab1,  tab3 = st.tabs(["📊 Data Explorer", "🕵️ Bias Detection"])
    
    with tab1:
        st.subheader("Citizen Database")
        st.dataframe(df.head())
        
        col1, col2 = st.columns(2)
        with col1:
             st.markdown("### Demographics")
             fig, ax = plt.subplots()
             df['Origin'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
             st.pyplot(fig)
        with col2:
             st.markdown("### Employment Status")
             st.bar_chart(df['Employment'].value_counts())

    with tab3:
        st.subheader("Algorithmic Bias Audit (Fairlearn)")
        st.markdown("Running **Fairlearn** to evaluate fairness metrics across sensitive groups.")
        
        if st.button("Run Bias Analysis"):
            with st.spinner("Calculating fairness metrics..."):
                try:
                    # Run bias detection
                    detect_bias("scored_citizens.csv", "bias_report.csv")
                    results = pd.read_csv("bias_report.csv")
                    st.success("Analysis Complete!")
                    
                    st.markdown("""
                    ### 📖 Guide to Metrics
                    - **Selection Rate**: The percentage of people in this group who "Qualified" for housing (Score ≥ 600). 
                      *If one group has a much lower rate, they might be unfairly excluded.*
                    - **Average Score**: The average "Social Utility Score" (0-1000) for this group.
                    """)
                    
                    # Display results by sensitive feature
                    features = results['sensitive_feature'].unique()
                    
                    for feature in features:
                        st.markdown(f"--- \n### 🕵️ Analysis by {feature}")
                        feature_data = results[results['sensitive_feature'] == feature]
                        
                        # Display metrics table
                        display_cols = ['group_value', 'count', 'selection_rate', 'average_raw_score']
                        st.dataframe(feature_data[display_cols].style.format({
                            'selection_rate': "{:.2%}",
                            'average_raw_score': "{:.1f}"
                        }))
                        
                        # Calculate biggest disparity
                        max_sel = feature_data['selection_rate'].max()
                        min_sel = feature_data['selection_rate'].min()
                        disparity = max_sel - min_sel
                        
                        if disparity > 0.1: # 10% gap
                            disadvantaged_group = feature_data.loc[feature_data['selection_rate'].idxmin(), 'group_value']
                            st.warning(f"⚠️ **Disparity Detected**: The group '{disadvantaged_group}' has a selection rate {disparity:.1%} lower than the best group.")
                        
                        # Visualize Disparities
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Selection Rate (Qualified > 600)**")
                            st.caption("Higher is better. Dashed line is the overall average.")
                            fig, ax = plt.subplots(figsize=(6, 4))
                            sns.barplot(data=feature_data, x='group_value', y='selection_rate', ax=ax, palette="viridis", hue='group_value', legend=False)
                            ax.axhline(feature_data['overall_selection_rate'].iloc[0], color='r', linestyle='--', label='Overall Rate')
                            ax.set_ylim(0, 1)
                            # ax.legend() # Removed as legend=False in barplot hides hue legend, and we manually added line label but barplot might override
                            st.pyplot(fig)
                            
                        with col2:
                            st.markdown("**Average Social Utility Score**")
                            st.caption("Higher is better. Dashed line is the overall average.")
                            fig, ax = plt.subplots(figsize=(6, 4))
                            sns.barplot(data=feature_data, x='group_value', y='average_raw_score', ax=ax, palette="rocket", hue='group_value', legend=False)
                            ax.axhline(feature_data['overall_average_raw_score'].iloc[0], color='r', linestyle='--', label='Overall Avg')
                            # ax.legend()
                            st.pyplot(fig)

                except Exception as e:
                    st.error(f"An error occurred during bias detection: {e}")

