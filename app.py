import streamlit as st
import pandas as pd

st.set_page_config(page_title="FamilyPay", layout="wide")

# --------------------------

# SESSION STATES

# --------------------------

if "screen" not in st.session_state:
st.session_state.screen = "splash"

# --------------------------

# STYLES

# --------------------------

st.markdown("""

<style>

.main{
background-color:#2E5C87;
color:white;
}

.wallet{
font-size:60px;
text-align:center;
}

.center{
text-align:center;
}

.button{
padding:12px;
border-radius:10px;
background:white;
color:#2E5C87;
font-weight:bold;
}

.card{
background:white;
padding:15px;
border-radius:12px;
box-shadow:0 2px 10px rgba(0,0,0,0.15);
color:black;
}

</style>

""",unsafe_allow_html=True)

# --------------------------

# SPLASH SCREEN

# --------------------------

if st.session_state.screen == "splash":

```
st.markdown("<h1 class='center'>💳</h1>",unsafe_allow_html=True)

st.markdown("<h1 class='center'>FamilyPay</h1>",unsafe_allow_html=True)

st.markdown("<p class='center'>India's first whole-family financial wallet.<br>Built for everyone.</p>",unsafe_allow_html=True)

if st.button("Get Started"):
    st.session_state.screen = "login"
    st.rerun()
```

# --------------------------

# LOGIN SCREEN

# --------------------------

elif st.session_state.screen == "login":

```
st.title("Secure Login")

phone = st.text_input("Enter Mobile Number","+91 98765 43210")

if st.button("Login with OTP"):
    st.session_state.screen = "dashboard"
    st.rerun()
```

# --------------------------

# DASHBOARD

# --------------------------

elif st.session_state.screen == "dashboard":

```
st.title("Family Dashboard")

st.metric("Family Wallet Balance","₹45,230")

st.divider()
```

# --------------------------

# QUICK ACTIONS

```
col1,col2,col3,col4 = st.columns(4)

col1.button("➕ Add Money")
col2.button("📤 Send")
col3.button("⚙ Limits")
col4.button("📄 Report")

st.divider()
```

# --------------------------

# MEMBER CARDS

```
st.subheader("Family Spending")

col1,col2,col3 = st.columns(3)

col1.markdown("""
<div class="card">
<b>Rajesh</b><br>
₹12,500<br>
No limit set
</div>
""",unsafe_allow_html=True)

col2.markdown("""
<div class="card">
<b>Priya</b><br>
₹8,300<br>
No limit set
</div>
""",unsafe_allow_html=True)

col3.markdown("""
<div class="card">
<b>Aryan</b><br>
₹2,500<br>
Limit ₹3000
</div>
""",unsafe_allow_html=True)

st.divider()
```

# --------------------------

# GOAL

```
st.subheader("Shared Goal Focus")

st.write("Goa Trip")

st.progress(0.6)

st.write("₹15,000 of ₹25,000")

st.divider()
```

# --------------------------

# TRANSACTIONS

```
st.subheader("Recent Transactions")

data = pd.DataFrame({
"Merchant":["Swiggy","Big Bazaar","Uber","Apollo Pharmacy"],
"Member":["Aryan","Priya","Rajesh","Dadaji"],
"Amount":["₹350","₹1200","₹540","₹220"]
})

st.table(data)
```
