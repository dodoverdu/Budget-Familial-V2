import streamlit as st
import pandas as pd

from core.belfius import lire_transactions
from core.categorisation import (
    categoriser,
    ajouter_regle
)
# ======================================================
# Configuration
# ======================================================

st.set_page_config(
    page_title="Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Assistant de catégorisation")

# ======================================================
# Chargement des transactions
# ======================================================

transactions = lire_transactions()
transactions = categoriser(transactions)

a_classer = transactions[
    transactions["Catégorie"] == "❓ A classer"
].copy()

if len(a_classer) == 0:
    st.success("🎉 Toutes les transactions sont classées !")
    st.stop()

transaction = a_classer.iloc[0]

# ======================================================
# Chargement des catégories
# ======================================================

regles = pd.read_csv(
    "data/categories.csv",
    sep=";",
    encoding="utf-8"
)

categories = sorted(
    regles["Catégorie"]
    .dropna()
    .unique()
)

# ======================================================
# Affichage transaction
# ======================================================

st.info(f"Transaction 1 / {len(a_classer)}")

col1, col2 = st.columns(2)

with col1:

    st.write("### Compte")
    st.write(transaction["Compte"])

    st.write("### Date")
    st.write(transaction["Date"].strftime("%d/%m/%Y"))

    st.write("### Montant")
    st.write(f"{transaction['Montant']:.2f} €")

with col2:

    st.write("### Contrepartie")
    st.write(transaction["Contrepartie"])

    st.write("### Libellé")
    st.write(transaction["Libellé"])

    st.write("### Communication")
    st.write(transaction["Communication"])

st.divider()

# ======================================================
# Choix catégorie
# ======================================================

categorie = st.selectbox(
    "Catégorie",
    categories
)

sous_categories = sorted(

    regles.loc[
        regles["Catégorie"] == categorie,
        "Sous-catégorie"
    ]

    .dropna()
    .unique()

)

sous_categorie = st.selectbox(
    "Sous-catégorie",
    sous_categories
)

creer_regle = st.checkbox(
    "Créer une règle automatiquement",
    value=True
)

if st.button("💾 Enregistrer et suivant"):

    if creer_regle:

        ajouter_regle(
            colonne="Contrepartie",
            valeur=str(transaction["Contrepartie"]).strip(),
            categorie=categorie,
            sous_categorie=sous_categorie
        )

        st.success("✅ Règle enregistrée dans categories.csv")
        
        st.rerun()
