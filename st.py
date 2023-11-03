import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Plotting function
st.image('https://raw.githubusercontent.com/xzrarcher/CMSE830/main/st.png')

st.title('Bank Marketing Data Exploration：what kind of people will survive under another crisis?')

st.markdown("""
In 2023, the world economy seems to be stuck in a rut. More and more economists are making pessimistic expectations about the future development of the global economy. With such a recession, it is highly likely that we will face another financial crisis in the next few years, like the one that happened in 2008, or even worse, the Great Depression of the 1920s. In this case, what kind of people have a higher probability of surviving and what kind of people have a higher probability of weathering future crises smoothly is the research direction of this project. We used customer information submitted by several European banks, including their occupations, incomes, deposits, educational backgrounds, etc., to try to analyze which groups of people would have a higher chance of receiving a smaller shock in a future financial crisis.
""")


st.markdown("""
    ## Detailed Analysis and Observations

    - **Age Distribution**: The majority of clients are in their 30s to 40s, indicating a market that is largely middle-aged. The distribution shows a normal curve but is slightly skewed towards the middle-aged group.
    - **Job Distribution**: The predominant sector is 'blue-collar', followed by 'management' and 'technician', suggesting these are the primary market segments that the bank services are catered to.
    - **Contact Duration & Term Deposits**: Clients who subscribed to term deposits ('yes') had significantly longer calls during the last contact. This insight could imply a strong correlation between successful conversions and the quality and length of customer interactions.
    - **Annual Average Balance Distribution**: A large number of clients have an average annual balance close to zero, with only a few outliers having a very high balance. The chart is limited to balances under 5000 for a clearer visualization of the main clusters.
    """)

def plot_data(data):
    sns.set(style="whitegrid")
    plt.rcParams.update({'font.size': 12})

    fig, axes = plt.subplots(2, 2, figsize=(20, 15))

    # 1. Age distribution
    ax1 = axes[0, 0]
    sns.histplot(data['age'], bins=30, kde=True, color='skyblue', ax=ax1)
    ax1.set_title('Age Distribution')
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Frequency')

    # 2. Job distribution
    ax2 = axes[0, 1]
    sns.countplot(y='job', data=data, order=data['job'].value_counts(
    ).index, palette='viridis', ax=ax2)
    ax2.set_title('Job Distribution')
    ax2.set_xlabel('Count')
    ax2.set_ylabel('Job Type')

    # 3. Contact Duration vs. Subscription to Term Deposit
    ax3 = axes[1, 0]
    sns.boxplot(x='y', y='duration', data=data, palette='viridis', ax=ax3)
    ax3.set_title('Contact Duration vs. Subscription to Term Deposit')
    ax3.set_xlabel('Term Deposit Subscribed')
    ax3.set_ylabel('Last Contact Duration (seconds)')

    # 4. Balance distribution
    ax4 = axes[1, 1]
    balance_data = data[data['balance'] <=
                        data['balance'].quantile(0.95)]  # 限制为95th分位数以下
    sns.histplot(balance_data['balance'], bins=30,
                 kde=True, color='skyblue', ax=ax4)
    ax4.set_title('Annual Average Balance Distribution')
    ax4.set_xlabel('Balance')
    ax4.set_ylabel('Frequency')

    plt.tight_layout()
    return plt.gcf()  # back to plot



def main():
    st.title("Bank Marketing Data Exploration")

    # sidebar
    st.sidebar.header("Data Insights")
    selected_option = st.sidebar.selectbox(
        "Choose the data point for insights",
        options=["", "Age", "Balance", "Day", "Duration", "Campaign", "Pdays", "Previous", "Job",
                 "Marital", "Education", "Default", "Housing", "Loan", "Contact", "Month", "Poutcome", "Y"],
        index=0  # default selection is the first blank option
    )

    # Display related text analysis based on the selected option
    if selected_option:
        st.sidebar.subheader(f"Insights for {selected_option}")

        # Detailed analysis for each data point
        insights_text = {
            "Age": "The average age of customers is around 41 years, with the youngest customer being 18 and the oldest 95.",
            "Balance": "The average balance is approximately 1,362, with a minimum of -8,019 (possibly indicating loans or overdrafts) and a maximum of 102,127.",
            "Day": "Contact days are distributed throughout the month from 1 to 31 days.",
            "Duration": "The average duration of the last contact is about 258 seconds, with the shortest being 0 seconds and the longest 4,918 seconds.",
            "Campaign": "The number of contacts with a customer during this campaign averages 2.76 times, with a maximum of 63 times.",
            "Pdays": "The average number of days after the previous campaign is 40 days, but the median and third quartile are -1 (possibly indicating no previous contact), with a maximum of 871 days.",
            "Previous": "The number of contacts with a customer before this campaign averages 0.58 times, with a maximum of 275 times.",
            "Job": "Most customers are engaged in blue-collar jobs, followed by management and technician roles. Only a few customers have an unknown job type.",
            "Marital": "A majority of customers are married.",
            "Education": "Most customers have received secondary education, followed by tertiary education. A small portion of customers has an unknown education level.",
            "Default": "The vast majority of customers have no default credit.",
            "Housing": "The data shows a significant portion of customers (more than half of the total) have housing loans. This may reflect the commonality of housing loans among the general population or a target market for specific bank products or services.",
            "Loan": "Most customers do not have personal loans, indicating that most customers are either at a relatively low level of debt or might not have requirements for loans.",
            "Contact": "'Cellular' (i.e., mobile phone) is the most common means of contact, indicating that mobile phones might be the most effective method of communication with customers. In contrast, fewer customers are contacted via 'telephone', and a significant portion is 'unknown', possibly a limitation in the data collection process where the means of contact were not recorded.",
            "Month": "'May' witnesses the most customer contacts, far exceeding other months. This might characterize bank marketing campaigns that intensify in May. However, it also raises questions about the effectiveness of campaigns in this month as it might also correlate with specific seasonal trends.",
            "Poutcome": "In most cases, the outcome of the previous marketing campaign is 'unknown', indicating these customers might be contacted for the first time. However, understanding whether the previous marketing campaigns were successful or not could be crucial for understanding customer responses and future marketing strategies.",
            "Y": "The vast majority of customers have not subscribed to a term deposit, suggesting a relatively low conversion rate or insufficient attractiveness of this specific product to customers."
        }

        # Display detailed analysis of the selected feature
        st.sidebar.write(insights_text[selected_option])

    # Loding data
    @st.cache_data  # update cache
    def load_data():
        url = "https://raw.githubusercontent.com/xzrarcher/CMSE830/main/bank-full.csv"
        data = pd.read_csv(url, sep=";")
        return data

    data = load_data()

 # Display a section title for the dataset preview
    st.header('Dataset Preview')

# Display the first few rows of the dataset
    st.dataframe(data.head())
    
    # Title
    st.header("Descriptive Analysis")

    # Plot in streamlit
    fig = plot_data(data)
    st.pyplot(fig)

    # Custom plot section
    st.header("Custom Plot Section")

    # selectbox
    st.sidebar.header("Create Your Own Plot")
    plot_types = ["Scatter Plot", "Line Plot", "Histogram", "Box Plot"]
    selected_plot = st.sidebar.selectbox("Select Plot Type", plot_types)
    selected_x = st.sidebar.selectbox("Select X Axis", data.columns)
    selected_y = st.sidebar.selectbox("Select Y Axis", data.columns)

    # plot based on user selection
    if st.sidebar.button("Generate Plot"):
        st.subheader(f"{selected_plot} between {selected_x} and {selected_y}")
        fig, ax = plt.subplots()
        if selected_plot == "Scatter Plot":
            sns.scatterplot(x=selected_x, y=selected_y, data=data, ax=ax)
        elif selected_plot == "Line Plot":
            sns.lineplot(x=selected_x, y=selected_y, data=data, ax=ax)
        elif selected_plot == "Histogram":

            sns.histplot(data[selected_x], kde=True, bins=30, ax=ax)
        elif selected_plot == "Box Plot":
            sns.boxplot(x=selected_x, y=selected_y, data=data, ax=ax)

        ax.set_title(f"{selected_plot} of {selected_x} vs {selected_y}")
        st.pyplot(fig)

    st.markdown("""
    ## Data Field Descriptions

    Before exploring the dataset, it's important to understand what each field represents. Below is a brief description of each:

    - **age**: The age of the client.
    - **job**: The type of job the client has.
    - **marital**: The marital status of the client.
    - **education**: The level of education of the client.
    - **default**: Indicates whether the client has credit in default.
    - **balance**: The yearly average balance, in euros, of the client.
    - **housing**: Indicates whether the client has a housing loan.
    - **loan**: Indicates whether the client has a personal loan.
    - **contact**: The type of communication used to contact the client.
    - **day**: The last contact day of the month with the client.
    - **month**: The last contact month of the year with the client.
    - **duration**: The duration, in seconds, of the last contact with the client.
    - **campaign**: The number of contacts performed during this campaign for this client.
    - **pdays**: The number of days that passed by after the client was last contacted from a previous campaign.
    - **previous**: The number of contacts performed before this campaign for this client.
    - **poutcome**: The outcome of the previous marketing campaign.
    - **y**: Indicates whether the client has subscribed to a term deposit (the response variable).

    Now, let's proceed with the analysis, visualizing these fields and their relationships.
    """)


if __name__ == "__main__":
    main()
