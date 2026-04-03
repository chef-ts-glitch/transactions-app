# source venv/bin/activate
# selecting python interpreter: ./venv/bin/python
import streamlit as st
import pandas as pd
import duckdb
import requests

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
REST_URL = f"{SUPABASE_URL}/rest/v1/transactions"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Transaction Analyzer", layout="centered")
st.title("💳 Transaction Analytics")

@st.cache_data
def load_data():
    try:
        r = requests.get(REST_URL, headers=HEADERS)
        r.raise_for_status()
        df = pd.DataFrame(r.json())
    except requests.exceptions.RequestException:
        df = pd.read_excel("transactions.xlsx")
    if df.empty:
        return df
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["amount"] = pd.to_numeric(df["amount"])
    return df

df = load_data()

if df.empty:
    st.warning("No data found in Supabase.")
    st.stop()

con = duckdb.connect(database=":memory:")
con.register("transactions", df)

merchant = st.selectbox(
    "Select Merchant",
    sorted(df["merchant"].dropna().unique())
)

date_range = st.date_input(
    "Select Date Range",
    value=(df["date"].min(), df["date"].max())
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

query = """
SELECT
    ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)) AS total_spent,
    SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS total_earned,
    SUM(amount) AS net
FROM transactions
WHERE merchant = ?
AND date BETWEEN ? AND ?;
"""

result = con.execute(query, [merchant, start_date, end_date]).fetchdf()
spent = result["total_spent"][0] or 0
earned = result["total_earned"][0] or 0
net = result["net"][0] or 0

st.subheader(f"📊 Summary for {merchant}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"₹{spent:,.2f}")
col2.metric("Total Earned", f"₹{earned:,.2f}")
col3.metric("Net", f"₹{net:,.2f}")

st.subheader("🧾 Transactions")
filtered_df = df[
    (df["merchant"] == merchant) &
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

if filtered_df.empty:
    st.write("No records found")
else:
    st.dataframe(filtered_df, use_container_width=True)