# advanced_streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page config
st.set_page_config(page_title="Students Performance Analysis", layout="wide")

# Title
st.title("Students Performance Analysis Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your StudentsPerformance CSV file", type=["csv"])

if uploaded_file:
    # Load dataset
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Calculate average score
    df['average_score'] = df[['math_score', 'reading_score', 'writing_score']].mean(axis=1)

    # Pass/Fail based on average >= 50
    df['result'] = df['average_score'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')

    # Histogram of average scores
    st.subheader("Average Score Distribution")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.histplot(data=df, x='average_score', hue='result', multiple='stack', 
                 palette={'Pass':'green','Fail':'red'}, ax=ax)
    ax.set_xlabel('Average Score')
    ax.set_ylabel('Number of Students')
    st.pyplot(fig)

    # Scatter plot: Math vs Reading
    st.subheader("Math vs Reading Scores")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=df, x='math_score', y='reading_score', hue='result', 
                    palette={'Pass':'green','Fail':'red'}, s=100, ax=ax)
    ax.set_xlabel('Math Score')
    ax.set_ylabel('Reading Score')
    st.pyplot(fig)

    # Scatter plot: Math vs Writing
    st.subheader("Math vs Writing Scores")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=df, x='math_score', y='writing_score', hue='result', 
                    palette={'Pass':'green','Fail':'red'}, s=100, ax=ax)
    ax.set_xlabel('Math Score')
    ax.set_ylabel('Writing Score')
    st.pyplot(fig)

    # Outliers
    st.subheader("Outliers (High in one subject, Low in another)")
    outliers = df[((df['math_score'] > df['math_score'].median()) & 
                   (df['reading_score'] < df['reading_score'].median())) |
                  ((df['reading_score'] > df['reading_score'].median()) & 
                   (df['math_score'] < df['math_score'].median()))]

    if outliers.empty:
        st.write("No outliers found based on criteria.")
    else:
        st.dataframe(outliers)

    # Pass/Fail ratios by gender
    if 'gender' in df.columns:
        st.subheader("Pass/Fail Ratios by Gender")
        gender_stats = df.groupby('gender')['result'].value_counts(normalize=True).unstack()
        st.dataframe(gender_stats)

        fig, ax = plt.subplots(figsize=(8,6))
        gender_stats.plot(kind='bar', stacked=True, color=['red','green'], ax=ax)
        ax.set_ylabel('Proportion')
        st.pyplot(fig)
