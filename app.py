import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="UAC Healthcare Analytics",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------

st.title("UAC Healthcare Analytics Dashboard")
st.markdown("Healthcare Capacity & Care Load Monitoring System")

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data
def load_data():

    # Get project root folder
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Correct CSV path
   file_path = os.path.join(
    BASE_DIR,
    "outputs",
    "cleaned_uac_healthcare_data.csv"
)

    # Read CSV
    df = pd.read_csv(file_path)

    # Convert date
    df['Date'] = pd.to_datetime(df['Date'])

    return df

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df['Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Date'].max()
)

# Filter dataframe
filtered_df = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

# -------------------------------
# KPI SECTION
# -------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total System Load",
    int(filtered_df['Total_System_Load'].iloc[-1])
)

col2.metric(
    "Average Net Intake",
    round(filtered_df['Net_Daily_Intake'].mean(), 2)
)

col3.metric(
    "Average Volatility",
    round(filtered_df['Volatility_Index'].mean(), 2)
)

# -------------------------------
# TOTAL SYSTEM LOAD
# -------------------------------

st.subheader("Total System Load Over Time")

fig1 = px.line(
    filtered_df,
    x='Date',
    y='Total_System_Load',
    title='Total System Load'
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -------------------------------
# CBP VS HHS
# -------------------------------

st.subheader("CBP vs HHS Care Load")

fig2 = px.line(
    filtered_df,
    x='Date',
    y=['CBP_Custody', 'HHS_Care'],
    title='CBP vs HHS'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -------------------------------
# NET DAILY INTAKE
# -------------------------------

st.subheader("Net Daily Intake")

fig3 = px.line(
    filtered_df,
    x='Date',
    y='Net_Daily_Intake',
    title='Net Daily Intake'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -------------------------------
# BACKLOG TREND
# -------------------------------

st.subheader("Backlog Trend")

fig4 = px.line(
    filtered_df,
    x='Date',
    y='Backlog',
    title='Backlog Trend'
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -------------------------------
# DATA TABLE
# -------------------------------

st.subheader("Dataset Preview")

st.dataframe(filtered_df.tail())

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_uac_data.csv',
    mime='text/csv'
)

# -------------------------------
# SUCCESS MESSAGE
# -------------------------------

st.success("Dashboard Loaded Successfully!")