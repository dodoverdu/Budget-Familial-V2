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


def ajouter_regle(
    colonne,
    valeur,
    categorie,
    sous_categorie
):
    """
    Ajoute une règle dans le fichier categories.csv.
    """

    regles = charger_regles()

    nouvelle = pd.DataFrame([
        {
            "Colonne": colonne,
            "Valeur": valeur,
            "Catégorie": categorie,
            "Sous-catégorie": sous_categorie
        }
    ])

    regles = pd.concat(
        [regles, nouvelle],
        ignore_index=True
    )

    regles = regles.drop_duplicates()

    regles.to_csv(
        FICHIER,
        sep=";",
        index=False,
        encoding="utf-8"
    )

    print("Nombre de règles :", len(regles))
    print("=================================\n")


def categoriser(df):
    """
    Applique les règles de catégorisation.
    """

    df = df.copy()

    df["Catégorie"] = "❓ A classer"
    df["Sous-catégorie"] = ""

    regles = charger_regles()

    for _, regle in regles.iterrows():

        colonne = str(regle["Colonne"]).strip()
        valeur = str(regle["Valeur"]).strip().upper()

        if colonne not in df.columns:
            print(f"Colonne introuvable : {colonne}")
            continue

        masque = (
            df[colonne]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.contains(valeur, na=False)
        )

        nb = masque.sum()

        if nb > 0:
            print(f"{valeur} -> {nb} transaction(s)")

        df.loc[masque, "Catégorie"] = regle["Catégorie"]
        df.loc[masque, "Sous-catégorie"] = regle["Sous-catégorie"]

    return df