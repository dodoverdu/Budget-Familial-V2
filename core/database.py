from pathlib import Path
import sqlite3

DOSSIER_DATA = Path("data")
DOSSIER_DATA.mkdir(exist_ok=True)

BASE = DOSSIER_DATA / "budget.db"


def connexion():
    """
    Retourne une connexion SQLite.
    """
    return sqlite3.connect(BASE)


def creer_base():
    """
    Crée la base si elle n'existe pas.
    """

    conn = connexion()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT,
        compte TEXT,
        contrepartie TEXT,

        montant REAL,

        categorie TEXT,
        sous_categorie TEXT,

        libelle TEXT,
        communication TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS regles (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        colonne TEXT,
        valeur TEXT,

        categorie TEXT,
        sous_categorie TEXT
    )
    """)

    conn.commit()
    conn.close()