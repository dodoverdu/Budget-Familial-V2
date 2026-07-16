from pathlib import Path
import pandas as pd

FICHIER = Path("data/categories.csv")


def charger_regles():
    """
    Charge les règles de catégorisation.
    """

    if not FICHIER.exists():
        return pd.DataFrame(
            columns=[
                "Colonne",
                "Valeur",
                "Catégorie",
                "Sous-catégorie"
            ]
        )

    return pd.read_csv(
        FICHIER,
        sep=";",
        encoding="utf-8"
    )


def categoriser(df):
    """
    Ajoute automatiquement les colonnes
    Catégorie et Sous-catégorie.
    """

    df = df.copy()

    df["Catégorie"] = "❓ A classer"
    df["Sous-catégorie"] = ""

    regles = charger_regles()

    for _, regle in regles.iterrows():

        colonne = regle["Colonne"]
        valeur = str(regle["Valeur"]).upper()

        # Compatibilité avec les anciens noms Belfius
        correspondance = {
            "Nom contrepartie contient": "Contrepartie",
            "Transaction": "Libellé",
            "Communications": "Communication",
            "Compte": "Compte",
            "Montant": "Montant"
        }

        colonne = correspondance.get(colonne, colonne)

        if colonne not in df.columns:
            continue

        masque = (
            df[colonne]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.contains(valeur, na=False)
        )

        df.loc[masque, "Catégorie"] = regle["Catégorie"]
        df.loc[masque, "Sous-catégorie"] = regle["Sous-catégorie"]

    return df