import streamlit as st

from core.database import creer_base
from core.belfius import lire_transactions, lire_soldes
from core.categorisation import categoriser

# ======================================================
# Configuration
# ======================================================

st.set_page_config(
    page_title="Budget Familial",
    page_icon="💰",
    layout="wide"
)

# ======================================================
# Initialisation
# ======================================================

creer_base()

st.title("💰 Budget Familial")

# ======================================================
# Fonctions d'affichage
# ======================================================

def format_montant(valeur):
    return (
        f"{valeur:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
        + " €"
    )


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
        format_montant(patrimoine)
    )

with col2:
    st.metric(
        "💸 Dépenses",
        format_montant(depenses)
    )

with col3:
    st.metric(
        "💵 Recettes",
        format_montant(recettes)
    )

with col4:
    st.metric(
        "📄 Transactions",
        f"{nb_transactions:,}".replace(",", " ")
    )

st.divider()

# ======================================================
# Situation bancaire
# ======================================================

st.subheader("🏦 Situation bancaire")

soldes_affichage = soldes.copy()

soldes_affichage["Solde"] = soldes_affichage["Solde"].apply(format_montant)

st.dataframe(
    soldes_affichage,
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
    .copy()
)

dernieres["Date"] = dernieres["Date"].dt.strftime("%d/%m/%Y")

dernieres["Montant"] = dernieres["Montant"].apply(format_montant)

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