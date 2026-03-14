import streamlit as st
import pandas as pd

st.set_page_config(page_title="FamilyPay", layout="wide")

st.title("💳 FamilyPay")
st.subheader("Sharma Family Dashboard")

# Wallet balance
st.metric("Total Family Wallet Balance", "₹45,230")

st.divider()

# Family members spending
st.header("Family Members Spending")

members = {
    "Rajesh (Admin)": 7450,
    "Priya (Spouse)": 5120,
    "Aryan (Teen)": 2100,
    "Neha (Child)": 900,
    "Dadaji (Elder)": 650
}

for member, amount in members.items():
    st.write(f"👤 **{member}** spent ₹{amount} this month")

st.divider()

# Transactions
st.header("Recent Transactions")

transactions = {
    "Member": ["Aryan","Priya","Rajesh","Neha","Dadaji"],
    "Merchant": ["Swiggy","Big Bazaar","KSRTC","Apollo Pharmacy","Medical Store"],
    "Amount (₹)": [250,1240,540,120,300]
}

df = pd.DataFrame(transactions)

st.table(df)

st.divider()

# Savings goals
st.header("Family Savings Goals")

st.write("🎯 Goa Trip")
st.progress(0.56)
st.write("₹14,000 / ₹25,000")

st.write("🎯 New TV")
st.progress(0.40)
st.write("₹20,000 / ₹50,000")

st.write("🎯 School Fees")
st.progress(0.40)
st.write("₹12,000 / ₹30,000")
