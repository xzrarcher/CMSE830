import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
df = pd.read_csv(url, names=columns)


# Title of the app
st.title("Heart Disease Data Explorer")


# Title of the app
# Let the user select columns for x and y axis
x_axis = st.selectbox("Select a column for x-axis", df.columns.tolist())
y_axis = st.selectbox("Select a column for y-axis", df.columns.tolist())
plot_type = st.selectbox("Select plot type", ["scatter", "line", "box", "violin", "heatmap"])



# Draw the corresponding plot
st.subheader(f"{plot_type.capitalize()} Plot for {y_axis} vs {x_axis}")
if plot_type == "scatter":
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=df[x_axis], y=df[y_axis])
    st.pyplot(fig)
elif plot_type == "line":
    fig, ax = plt.subplots()
    ax = sns.lineplot(x=df[x_axis], y=df[y_axis])
    st.pyplot(fig)
elif plot_type == "box":
    fig, ax = plt.subplots()
    ax = sns.boxplot(x=df[x_axis], y=df[y_axis])
    st.pyplot(fig)
elif plot_type == "violin":
    fig, ax = plt.subplots()
    ax = sns.violinplot(x=df[x_axis], y=df[y_axis])
    st.pyplot(fig)
elif plot_type == "heatmap":
    fig, ax = plt.subplots(figsize=(10,8))
    ax = sns.heatmap(df[[x_axis, y_axis]].corr(), annot=True, cmap='coolwarm')
    st.pyplot(fig)
