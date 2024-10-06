import streamlit as st
import pandas as pd
import os
from pandasai import Agent
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the Streamlit page
st.set_page_config(page_title="CSV Analyzer with PandasAI", page_icon="📊", layout="wide")
st.title("CSV Analyzer with PandasAI")

# Set PandasAI API key from environment variable or directly
os.environ["PANDASAI_API_KEY"] = "$2a$10$Pu3J46EGjy1x76wgFPlKY.9VOgxEUnXAJXSNcqRylMEFuZDCi.25u"  # Replace with your actual API key

# File uploader for CSV input
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df.head())

    # Initialize PandasAI Agent
    agent = Agent(df)

    # User query input
    user_query = st.text_input('''use "plot" in prompt to generate graph''')

    if user_query:
        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                try:
                    # Get response from PandasAI
                    response = agent.chat(user_query)
                    st.write("Analysis Result:")
                    st.write(response)

                    # Generate additional visualizations based on query
                    if "Plot" in user_query or "plot" in user_query:
                        fig, ax = plt.subplots(figsize=(10, 6))

                        # Assuming user asks for a bar plot (you can extend this based on needs)
                        if "histogram" in user_query or "bar" in user_query:
                            sns.barplot(x=df.iloc[:, 0], y=df.iloc[:, 1], ax=ax, palette="Set2")
                            ax.set_title(f"Histogram/Bar plot for {df.columns[0]} vs {df.columns[1]}")
                            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

                        # Show the plot
                        st.pyplot(fig)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to get started.")

