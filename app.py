import streamlit as st

from belfius import lire_transactions, lire_soldes
from categorisation import categoriser

# ======================================================
# Configuration
# ======================================================

st.set_page_config(
    page_title="Budget Familial",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Budget Familial")

# ======================================================
# Chargement des données
# ======================================================

soldes = lire_soldes()

transactions = lire_transactions()
transactions = categoriser(transactions)

# ======================================================
# KPI
# ======================================================

depenses = abs(
    transactions.loc[
        transactions["Montant"] < 0,
        "Montant"
    ].sum()
)

recettes = (
    transactions.loc[
        transactions["Montant"] > 0,
        "Montant"
    ].sum()
)

patrimoine = soldes["Solde"].sum()

nb_transactions = len(transactions)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Patrimoine",
        f"{patrimoine:,.2f} €"
    )

with col2:
    st.metric(
        "💸 Dépenses",
        f"{depenses:,.2f} €"
    )

with col3:
    st.metric(
        "💵 Recettes",
        f"{recettes:,.2f} €"
    )

with col4:
    st.metric(
        "📄 Transactions",
        nb_transactions
    )

st.divider()

# ======================================================
# Situation bancaire
# ======================================================

st.subheader("🏦 Situation bancaire")

st.dataframe(
    soldes,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ======================================================
# Dernières transactions
# ======================================================

st.subheader("📄 Dernières transactions")

dernieres = (
    transactions
    .sort_values("Date", ascending=False)
    .head(15)
)

st.dataframe(
    dernieres[
        [
            "Date",
            "Compte",
            "Contrepartie",
            "Montant",
            "Catégorie",
            "Sous-catégorie"
        ]
    ],
    use_container_width=True,
    hide_index=True
)