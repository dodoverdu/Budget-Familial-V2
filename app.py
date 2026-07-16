import streamlit as st

from belfius import lire_transactions
from belfius import lire_soldes

st.set_page_config(
    page_title="Budget Familial",
    page_icon="💰",
    layout="wide"
)

transactions = lire_transactions()
soldes = lire_soldes()

st.title("💰 Budget Familial")

st.header("🏦 Situation bancaire")

st.dataframe(
    soldes,
    use_container_width=True
)

st.metric(
    "💰 Total disponible",
    f"{soldes['Solde'].sum():,.2f} €"
)

st.divider()

st.header("📄 Transactions")

st.write(f"{len(transactions)} transactions")

st.dataframe(
    transactions,
    use_container_width=True
)