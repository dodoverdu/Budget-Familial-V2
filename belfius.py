from pathlib import Path
import pandas as pd
from config import COMPTES

DOSSIER_CSV = Path("data/csv")


def lire_fichiers():
    return sorted(DOSSIER_CSV.glob("*.csv"))


def lire_transactions():

    liste = []

    for fichier in lire_fichiers():

        df = pd.read_csv(
            fichier,
            sep=";",
            encoding="latin1",
            skiprows=12
        )

        liste.append(df)

    return pd.concat(liste, ignore_index=True)


def lire_soldes():

    comptes = []

    for fichier in lire_fichiers():

        with open(fichier, encoding="latin1") as f:
            lignes = f.readlines()

        # Récupération du dernier solde
        dernier_solde = lignes[9].split(";")[1]

        dernier_solde = (
            dernier_solde
            .replace(" EUR", "")
            .replace(".", "")
            .replace(",", ".")
        )

        # Recherche automatique de l'IBAN
        iban = ""

        for ligne in lignes:
            if ligne.startswith("BE"):
                iban = ligne.split(";")[0]
                break

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

    df = df.sort_values("Ordre").reset_index(drop=True)

    return df