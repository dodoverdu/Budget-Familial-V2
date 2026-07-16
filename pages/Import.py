from pathlib import Path
import streamlit as st

# ======================================================
# Configuration
# ======================================================

st.set_page_config(
    page_title="Import Belfius",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Import des relevés Belfius")

st.write(
    "Sélectionnez un ou plusieurs exports CSV Belfius. "
    "Ils seront copiés automatiquement dans le dossier de travail."
)

DOSSIER_DESTINATION = Path("data/csv")
DOSSIER_DESTINATION.mkdir(parents=True, exist_ok=True)

# ======================================================
# Sélection des fichiers
# ======================================================

fichiers = st.file_uploader(
    "Choisir les fichiers CSV Belfius",
    type=["csv"],
    accept_multiple_files=True
)

# ======================================================
# Import
# ======================================================

if fichiers:

    st.write(f"**{len(fichiers)} fichier(s) sélectionné(s)**")

    if st.button("📥 Importer"):

        nb_importes = 0

        for fichier in fichiers:

            destination = DOSSIER_DESTINATION / fichier.name

            with open(destination, "wb") as f:
                f.write(fichier.getbuffer())

            nb_importes += 1

        st.success(f"✅ {nb_importes} fichier(s) importé(s).")

        st.info(
            "Vous pouvez maintenant retourner sur le Dashboard "
            "ou la page Transactions."
        )