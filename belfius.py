from pathlib import Path
import pandas as pd
from config import COMPTES

DOSSIER_CSV = Path("data/csv")


def lire_fichiers():
    """
    Retourne uniquement les exports Belfius.
    """
    return sorted(DOSSIER_CSV.glob("BE*.csv"))


def lire_transactions():
    """
    Lit tous les exports Belfius.
    """

    liste = []

    for fichier in lire_fichiers():

        df = pd.read_csv(
            fichier,
            sep=";",
            encoding="latin1",
            skiprows=12
        )

        liste.append(df)

    transactions = pd.concat(liste, ignore_index=True)

    # ------------------------
    # Renommage des colonnes
    # ------------------------

    transactions = transactions.rename(columns={

        "Date de comptabilisation": "Date",
        "Nom contrepartie contient": "Contrepartie",
        "Transaction": "Libellé",
        "Communications": "Communication",
        "Compte": "Compte",
        "Montant": "Montant",
        "Compte contrepartie": "Compte contrepartie"

    })

    # ------------------------
    # Conversion des montants
    # ------------------------

    transactions["Montant"] = (
        transactions["Montant"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # ------------------------
    # Conversion des dates
    # ------------------------

    transactions["Date"] = pd.to_datetime(
        transactions["Date"],
        dayfirst=True,
        errors="coerce"
    )

    return transactions


def lire_soldes():

    comptes = []

    for fichier in lire_fichiers():

        with open(fichier, encoding="latin1") as f:
            lignes = f.readlines()

        iban = ""

        for ligne in lignes:
            if ligne.startswith("BE"):
                iban = ligne.split(";")[0].strip()
                break

        dernier_solde = (
            lignes[9]
            .split(";")[1]
            .replace(" EUR", "")
            .replace(".", "")
            .replace(",", ".")
        )

        infos = COMPTES.get(
            iban,
            {
                "nom": iban,
                "type": "Inconnu",
                "ordre": 999
            }
        )

        comptes.append({
            "Ordre": infos["ordre"],
            "Compte": infos["nom"],
            "Type": infos["type"],
            "IBAN": iban,
            "Solde": float(dernier_solde)
        })

    df = pd.DataFrame(comptes)

    return (
        df
        .sort_values("Ordre")
        .drop(columns="Ordre")
        .reset_index(drop=True)
    )