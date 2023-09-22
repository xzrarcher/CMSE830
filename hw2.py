import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px

df_iris = sns.load_dataset("iris")

# Display text to describe the dataset
st.write("""
# Iris Dataset
Explore the Iris dataset by examining the relationship between sepal length, sepal width, and petal length.
""")

# Create a 3D scatter plot using Plotly
fig = px.scatter_3d(df_iris, x='sepal_length', y='sepal_width', z='petal_length',
                     color='species', symbol='species',
                     title='Iris Dataset: Sepal Length vs Sepal Width vs Petal Length',
                     labels={'sepal_length': 'Sepal Length', 'sepal_width': 'Sepal Width', 'petal_length': 'Petal Length'},
                     width=700, height=700)

# Display the plot
st.plotly_chart(fig)