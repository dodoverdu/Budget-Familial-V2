import streamlit as st
import pandas as pd
from pathlib import Path

FICHIER = Path("data/categories.csv")

st.set_page_config(
    page_title="Règles",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Règles de catégorisation")

# ======================================================
# Chargement
# ======================================================

if FICHIER.exists():

    regles = pd.read_csv(
        FICHIER,
        sep=";",
        encoding="utf-8"
    )

else:

    regles = pd.DataFrame(
        columns=[
            "Colonne",
            "Valeur",
            "Catégorie",
            "Sous-catégorie"
        ]
    )

# ======================================================
# Tableau
# ======================================================

st.subheader("Règles existantes")

st.dataframe(
    regles,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ======================================================
# Nouvelle règle
# ======================================================

st.subheader("Nouvelle règle")

col1, col2 = st.columns(2)

with col1:

    valeur = st.text_input(
        "Valeur recherchée",
        placeholder="Ex : AMAZON"
    )

    categorie = st.text_input(
        "Catégorie",
        placeholder="Ex : Shopping"
    )

with col2:

    colonne = st.selectbox(
        "Colonne",
        [
            "Contrepartie",
            "Communication",
            "Libellé"
        ]
    )

    sous_categorie = st.text_input(
        "Sous-catégorie",
        placeholder="Ex : Internet"
    )

# ======================================================
# Enregistrement
# ======================================================

if st.button("💾 Ajouter la règle"):

    if valeur and categorie:

        nouvelle = pd.DataFrame([{

            "Colonne": colonne,
            "Valeur": valeur.upper(),
            "Catégorie": categorie,
            "Sous-catégorie": sous_categorie

        }])

        regles = pd.concat(
            [regles, nouvelle],
            ignore_index=True
        )

        regles.to_csv(
            FICHIER,
            sep=";",
            index=False,
            encoding="utf-8"
        )

        st.success("Règle enregistrée.")

        st.rerun()

    else:

        st.warning("Complète au minimum Valeur et Catégorie.")