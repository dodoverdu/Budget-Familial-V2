import streamlit as st

from belfius import lire_transactions
from categorisation import categoriser

# ======================================================
# Configuration
# ======================================================

st.set_page_config(
    page_title="Transactions",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Transactions")

# ======================================================
# Fonctions
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

transactions = lire_transactions()
transactions = categoriser(transactions)

# ======================================================
# Filtres
# ======================================================

col1, col2, col3 = st.columns(3)

with col1:

    recherche = st.text_input(
        "🔍 Recherche",
        placeholder="Mango, Renmans, Coolblue..."
    )

with col2:

    compte = st.selectbox(
        "💳 Compte",
        ["Tous"] + sorted(transactions["Compte"].unique())
    )

with col3:

    categorie = st.selectbox(
        "🏷 Catégorie",
        ["Toutes"] + sorted(transactions["Catégorie"].unique())
    )

# ======================================================
# Application des filtres
# ======================================================

df = transactions.copy()

if recherche:

    masque = (
        df["Contrepartie"]
        .fillna("")
        .str.contains(recherche, case=False)
    )

    df = df[masque]

if compte != "Tous":
    df = df[df["Compte"] == compte]

if categorie != "Toutes":
    df = df[df["Catégorie"] == categorie]

# ======================================================
# Préparation affichage
# ======================================================

df = df.sort_values("Date", ascending=False)

df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

df["Montant"] = df["Montant"].apply(format_montant)

# ======================================================
# Résultat
# ======================================================

st.caption(f"{len(df)} transaction(s)")

st.dataframe(

    df[
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