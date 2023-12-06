import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import os
from model_coefficients import coefficients


st.markdown("# American Housing Price Prediction App")
st.markdown("This app allows you to enter your house features and returns the estimated price of your house in USD.")
st.markdown("## Features that affect the price of your house")
st.markdown("""You may want to know what features affect the price of your house. We used the dataset from Kaggle, which contains 13 explanatory variables describing (almost) every aspect of residential homes.
The dataset can be found [here](https://www.kaggle.com/datasets/camnugent/california-housing-price). We used a simple Linear Regression model to predict the price of the house.
The model is not perfect, but it can give you a rough idea of how much your house is worth. Below are the feature importances of the model. The higher the coefficient, 
the more important the feature is. If the coefficient is negative, it means that the feature has a negative impact on the price of the house.""")



df = pd.DataFrame(coefficients, index=[0])
df = df.T.reset_index()
df.columns = ["Feature", "Coefficient"]
st.write(df, use_container_width=True)
st.bar_chart(df.set_index("Feature"))

# Load the data
@st.cache_data  # update cache
def load_data():
        url = "https://github.com/xzrarcher/CMSE830/blob/main/2/housing.csv"
        housing_df = pd.read_csv(url, sep=";")
        return data

categorical_cols = ["ocean_proximity"]
numerical_cols = [c for c in housing_df.columns if c not in categorical_cols and c != "median_house_value"]
# EDA
st.markdown("## Exploratory Data Analysis")
st.markdown("### Data Preview")
st.write(housing_df.head())

# Correlation matrix
st.markdown("### Correlation Matrix")
data = housing_df[numerical_cols].corr()
# heatmap
fig, ax = plt.subplots()
sns.heatmap(data, annot=True, ax=ax)
st.pyplot(fig)


st.markdown("## Plot feature vs. price")
# A dropdown menu to select the feature
feature = st.selectbox("Select a feature", housing_df.columns)

# Create a scatter plot with regression line
fig, ax = plt.subplots()
if feature in categorical_cols:
    sns.boxplot(x=feature, y="median_house_value", data=housing_df, ax=ax)
    ax.set_xlabel(feature)
    ax.set_ylabel("median_house_value")
else:
    sns.regplot(x=feature, y="median_house_value", data=housing_df, ax=ax)
    ax.set_xlabel(feature)
    ax.set_ylabel("median_house_value")
st.pyplot(fig)

st.markdown("## Predict the price of your house")
st.markdown("Please enter your house features below.")

longitude = st.number_input("longitude", value=-122.23)
latitude = st.number_input("latitude", value=37.88)
housing_median_age = st.number_input("housing_median_age", value=41)
total_rooms = st.number_input("total_rooms", value=880)
total_bedrooms = st.number_input("total_bedrooms", value=129)
population = st.number_input("population", value=322)
households = st.number_input("households", value=126)
median_income = st.number_input("median_income", value=8.3252)
median_house_value = st.number_input("median_house_value", value=452600)
ocean_proximity = st.selectbox("ocean_proximity", housing_df["ocean_proximity"].unique())

# Convert the ocean_proximity to numerical
x_df = pd.DataFrame({
    "longitude": [longitude],
    "latitude": [latitude],
    "housing_median_age": [housing_median_age],
    "total_rooms": [total_rooms],
    "total_bedrooms": [total_bedrooms],
    "population": [population],
    "households": [households],
    "median_income": [median_income],
    "median_house_value": [median_house_value],
    "ocean_proximity": [ocean_proximity]
})
x_df["ocean_proximity_INLAND"] = (x_df["ocean_proximity"] == "INLAND").astype(int)
x_df["ocean_proximity_ISLAND"] = (x_df["ocean_proximity"] == "ISLAND").astype(int)
x_df["ocean_proximity_NEAR BAY"] = (x_df["ocean_proximity"] == "NEAR BAY").astype(int)
x_df["ocean_proximity_NEAR OCEAN"] = (x_df["ocean_proximity"] == "NEAR OCEAN").astype(int)
x_df["ocean_proximity_<1H OCEAN"] = (x_df["ocean_proximity"] == "<1H OCEAN")

keys = ["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households",
        "median_income", "ocean_proximity_INLAND", "ocean_proximity_ISLAND",
        "ocean_proximity_NEAR BAY", "ocean_proximity_NEAR OCEAN"]
x = np.array(x_df[keys]).ravel()
beta = np.array([coefs[k] for k in keys])
intercept = coefs["intercept"]
price = x.dot(beta) + intercept
st.markdown(f"## The estimated price of your house is ${price:,.2f}")

# Add side bar
st.sidebar.markdown("## Get Description about Features")
# dropdown menu
feature = st.sidebar.selectbox("Select a feature", housing_df.columns, key="sidebar")
# show description

# Set up the descriptions
desc = {
    "longitude": "longitude",
    "latitude": "latitude",
    "housing_median_age": "median age of a house within a block",
    "total_rooms": "total number of rooms within a block",
    "total_bedrooms": "total number of bedrooms within a block",
    "population": "total number of people residing within a block",
    "households": "total number of households, a group of people residing within a home unit, for a block",
    "median_income": "median income for households within a block of houses (measured in tens of thousands of US Dollars)",
    "median_house_value": "median house value for households within a block (measured in US Dollars)",
    "ocean_proximity": "location of the house w.r.t ocean/sea"
}
st.sidebar.markdown(desc[feature])

# Descriptive statistics
st.sidebar.markdown("## Descriptive Statistics")
st.sidebar.markdown("### Numerical Features")
st.sidebar.write(housing_df[numerical_cols].describe())
st.sidebar.markdown("### Categorical Features")
st.sidebar.write(housing_df[categorical_cols].describe())
