import streamlit as st
import pandas as pd

# Page title
st.title("UAC HEALTHCARE ANALYTICS DASHBOARD")

# Load dataset
df = pd.read_csv("reports/HHS_Unaccompanied_Alien_Children_Program.csv")
# Show original columns
st.write("Original Columns:", df.columns)

# Keep first 6 columns only
df = df.iloc[:, :6]

# Rename columns
df.columns = [
    'Date',
    'CBP_Intake',
    'CBP_Custody',
    'Transferred_to_HHS',
    'HHS_Care',
    'Discharged'
]

# Convert date column
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df = df.sort_values('Date')

# Numeric columns
numeric_cols = [
    'CBP_Intake',
    'CBP_Custody',
    'Transferred_to_HHS',
    'HHS_Care',
    'Discharged'
]

# Clean numeric values
for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '', regex=False)
    )

    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

# Fill missing values
df = df.ffill()

# Create metric
df['Total_System_Load'] = (
    df['CBP_Custody'] + df['HHS_Care']
)

# Dashboard sections
st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Key Metric")

st.metric(
    "Average System Load",
    round(df['Total_System_Load'].mean(), 2)
)

st.subheader("System Load Trend")

st.line_chart(
    df.set_index('Date')['Total_System_Load']
)

st.success("Dashboard Running Successfully!")