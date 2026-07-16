import streamlit as st

from core.database import connexion

st.set_page_config(
    page_title="Administration",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Administration")

conn = connexion()
cur = conn.cursor()

# Nombre de transactions
cur.execute("SELECT COUNT(*) FROM transactions")
nb_transactions = cur.fetchone()[0]

# Nombre de règles
cur.execute("SELECT COUNT(*) FROM regles")
nb_regles = cur.fetchone()[0]

st.metric(
    "Transactions en base",
    nb_transactions
)

st.metric(
    "Règles en base",
    nb_regles
)

st.divider()

st.subheader("Dernières transactions")

cur.execute("""
SELECT
    date,
    compte,
    contrepartie,
    montant,
    categorie
FROM transactions
ORDER BY id DESC
LIMIT 20
""")

lignes = cur.fetchall()

st.dataframe(
    lignes,
    use_container_width=True,
    hide_index=True
)

conn.close()