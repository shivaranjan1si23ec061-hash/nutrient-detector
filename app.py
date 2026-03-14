import streamlit as st
import pandas as pd

st.set_page_config(page_title="FamilyPay", layout="wide")

st.title("💳 FamilyPay")
st.subheader("Sharma Family Dashboard")

# Wallet Balance
st.metric("Total Family Balance", "₹45,230")

st.divider()

# Family Members
st.header("Family Members")

members = {
    "Rajesh (Admin)": 7450,
    "Priya (Spouse)": 5120,
    "Aryan (Teen)": 2100,
    "Neha (Child)": 900,
    "Dadaji (Elder)": 650
}

for m in members:
    st.write(f"👤 {m} - Spent ₹{members[m]} this month")

st.divider()

# Transactions
st.header("Recent Transactions")

data = {
    "Member": ["Aryan","Priya","Rajesh","Neha","Dadaji"],
    "Merchant": ["Swiggy","Big Bazaar","KSRTC","Apollo Pharmacy","Medical Store"],
    "Amount":[250,1240,540,120,300]
}

df = pd.DataFrame(data)

st.table(df)

st.divider()

# Savings Goals
st.header("Savings Goals")

st.write("🎯 Goa Trip")
st.progress(0.56)
st.write("₹14,000 / ₹25,000")

st.write("🎯 New TV")
st.progress(0.40)
st.write("₹20,000 / ₹50,000")

st.write("🎯 School Fees")
st.progress(0.40)
st.write("₹12,000 / ₹30,000")
