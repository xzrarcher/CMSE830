import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import os
from model_coefficients import coefs

tab1, tab2, tab3 = st.tabs(["Introduction", "Prediction", "About The Creator"])

with tab1:

    st.image('https://raw.githubusercontent.com/xzrarcher/CMSE830/main/2/house.jpg')
    st.markdown("# Welcome to the Premier House Price Analysis Tool")
    st.markdown("In an ever-evolving real estate landscape, accurate and strategic decision-making is the key to success. We present to you our sophisticated House Price Analysis Tool, meticulously crafted to serve as your expert guide in navigating the complexities of the property market. Designed with precision and a user-centric approach, this tool is not just a technological marvel; it's a reflection of our deep commitment to empowering real estate enthusiasts, investors, and professionals.")
    st.markdown("## Why Choose Our Tool?")
    st.markdown(" Our solution stands out as a testament to our expertise in blending cutting-edge technology with practical market intelligence. It's not just about numbers; it's about providing a clear, actionable perspective that enhances your real estate journey.")

    st.markdown("""
    ## What This Tool Offers You:

    - **Precise Market Insights**: Leverage the latest in data analytics to gain a nuanced understanding of property values.
    - **Smart Investment Decisions**: Identify lucrative opportunities and make informed investment choices with confidence.
    - **Real-Time Data at Your Fingertips**: Stay ahead with up-to-the-minute market trends and analysis.
    """)
    st.markdown("""
         ## Embrace the Future of Real Estate Analysis:
            Embark on a journey of informed decision-making and strategic planning with our House Price Analysis Tool. We invite you to explore the possibilities and unlock the potential in every real estate venture.
        """)

    st.markdown("""
## Discover the Key Drivers Influencing Your Home's Value

In the quest to understand the myriad factors that define a home's market value, we've harnessed a comprehensive dataset from Kaggle, encompassing 13 critical variables that paint a detailed picture of residential properties. This extensive dataset serves as the backbone of our analysis, and you can explore it in full [here](#).

At the heart of our tool lies a streamlined Linear Regression model, meticulously calibrated to offer a reliable estimation of your property's worth. While no model can claim absolute perfection, ours is designed to provide you with a well-rounded perspective on your home's market potential.

### Unveiling the Features That Matter Most:
Our model doesn't just predict prices; it sheds light on the 'why' and 'how' of property valuation. Each feature's coefficient in our model is a story in itself:
- **Positive Coefficients**: Indicators that elevate your property's value.
- **Negative Coefficients**: Elements that might be pulling down your home's price.

With this intuitive understanding, you're equipped not just with a figure but with insights into what drives that figure. Whether you're planning to sell, buy, or simply stay informed, our House Price Prediction Tool is your window into the nuanced world of real estate valuation.
""")

with tab2:

    df = pd.DataFrame(coefs, index=[0])
    df = df.T.reset_index()
    df.columns = ["Feature", "coefs"]
    st.write(df, use_container_width=True)
    st.bar_chart(df.set_index("Feature"))

# Load the data
# Corrected load_data function

    @st.cache  # Use @st.cache
    def load_data():
        url = "https://raw.githubusercontent.com/xzrarcher/CMSE830/main/2/housing.csv"
        housing_df = pd.read_csv(url)  # Assuming the file is a standard CSV
        return housing_df


# Call the function to load data
    housing_df = load_data()

    categorical_cols = ["ocean_proximity"]
    numerical_cols = [
        c for c in housing_df.columns if c not in categorical_cols and c != "median_house_value"]

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
    ocean_proximity = st.selectbox(
        "ocean_proximity", housing_df["ocean_proximity"].unique())

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
    x_df["ocean_proximity_INLAND"] = (
        x_df["ocean_proximity"] == "INLAND").astype(int)
    x_df["ocean_proximity_ISLAND"] = (
        x_df["ocean_proximity"] == "ISLAND").astype(int)
    x_df["ocean_proximity_NEAR BAY"] = (
        x_df["ocean_proximity"] == "NEAR BAY").astype(int)
    x_df["ocean_proximity_NEAR OCEAN"] = (
        x_df["ocean_proximity"] == "NEAR OCEAN").astype(int)
    x_df["ocean_proximity_<1H OCEAN"] = (
        x_df["ocean_proximity"] == "<1H OCEAN")

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
    feature = st.sidebar.selectbox(
        "Select a feature", housing_df.columns, key="sidebar")
    # show description

    # Set up the descriptions
    desc = {
        "longitude": "A measure of how far west a house is; a higher value is farther west",
        "latitude": "A measure of how far north a house is; a higher value is farther north",
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

with tab3:
    st.markdown("# About the Creator")
    resume_content = """
# About Me

## Contact Information
- **Email**: xuzhongr@msu.edu
- **GitHub**: [github.com/xzrarcher](#)

## Professional Summary
Passionate data scientist with extensive experience in machine learning, software development, and data analysis. Proven track record of leveraging data to drive business solutions. Proficient in Python, Rust, C, and C++ with a strong foundation in statistical analysis and model development.

## Skills
- **Programming Languages**: Python, Rust, C, C++
- **Machine Learning**: Regression, Classification, Clustering, Neural Networks, Transfomer, GAN, AutoML, NLP, Computer Vision, Time Series,   Reinforcement Learning
- **Data Analysis**: Pandas, NumPy, SciPy,  Scikit-Learn, PyTorch, TensorFlow, Keras, NLTK, OpenCV
- **Data Visualization**: Matplotlib, Seaborn, Altair,  Plotly, Tableau
- **Software Development**: Object-Oriented Programming, Agile Methodologies
- **Databases**: SQL, NoSQL
- **Other Tools**: Git, Docker, Jupyter

## Education

### PhD In Electrical Engineering
*Michigan States University 2022 - present*

### Bachelor of Engineering in Electrical Engineering and Computer Science
*Michigan States University 2017 - 2022*

## Hobbies & Interests
- Enthusiastic about playing video games and competitive tennis.
- Regular participant in coding hackathons and tech meetups.
- Avid reader of technology and data science blogs.


"""

# Display the resume using Streamlit's markdown function
st.markdown(resume_content)
