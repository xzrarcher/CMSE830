import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

# Load Data
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/xzrarcher/CMSE830/main/bank-additional-full.csv"
    df = pd.read_csv(url, sep=";")
    return df

# Main app
def app():
    df = load_data()

    st.title("Bank Marketing Data Exploration")

    # User selection
    st.sidebar.header("User Input Features")
    columns = df.columns.tolist()
    x_axis = st.sidebar.selectbox("Select X Axis", columns)
    y_axis = st.sidebar.selectbox("Select Y Axis", columns)
    selected_plots = st.sidebar.multiselect("Select Plots to Display", 
                                            ["Scatter Plot", "Violin Plot", "Box Plot", "Heatmap", "Histogram", "Count Plot", "Pair Plot"],
                                            default=["Scatter Plot"])

    num_prior_sessions = st.sidebar.slider("Select Number of Prior Sessions", 1, 10, 5)
    df_filtered = df[df['previous'] <= num_prior_sessions]
    
    # Display the selected plots using the filtered data
    if "Scatter Plot" in selected_plots:
        st.subheader("Scatter Plot")
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_filtered, x=x_axis, y=y_axis)
        plt.title(f"Scatter plot between {x_axis} and {y_axis}")
        st.pyplot(plt)
        
    if "Violin Plot" in selected_plots:
        st.subheader("Violin Plot")
        plt.figure(figsize=(8, 6))
        sns.violinplot(data=df_filtered, x=x_axis, y=y_axis)
        plt.title(f"Violin plot of {y_axis} vs {x_axis}")
        st.pyplot(plt)
        
    if "Box Plot" in selected_plots:
        st.subheader("Box Plot")
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df_filtered, x=x_axis, y=y_axis)
        plt.title(f"Box plot of {y_axis} vs {x_axis}")
        st.pyplot(plt)
        
    if "Heatmap" in selected_plots:
        st.subheader("Heatmap")
        plt.figure(figsize=(10, 7))
        sns.heatmap(df_filtered.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Feature Correlation Heatmap")
        st.pyplot(plt)
        
    if "Histogram" in selected_plots:
        st.subheader("Histogram with Normal Distribution")
        plt.figure(figsize=(8, 6))
        sns.histplot(df_filtered[x_axis], kde=True)
        
        # Plot normal distribution
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, df_filtered[x_axis].mean(), df_filtered[x_axis].std())
        plt.plot(x, p, 'k', linewidth=2)
        
        plt.title(f"Histogram of {x_axis} with Normal Distribution")
        st.pyplot(plt)
        
    if "Count Plot" in selected_plots:
        st.subheader("Count Plot")
        plt.figure(figsize=(8, 6))
        sns.countplot(data=df_filtered, x=x_axis)
        plt.title(f"Count Plot of {x_axis}")
        st.pyplot(plt)

    if "Pair Plot" in selected_plots:
        st.subheader("Pair Plot")
        selected_columns = st.multiselect("Select Columns for Pair Plot", columns, default=[x_axis, y_axis])
        plt.figure(figsize=(10, 7))
        sns.pairplot(df_filtered[selected_columns])
        plt.title("Pair Plot")
        st.pyplot(plt)

# Calling the function
app()
