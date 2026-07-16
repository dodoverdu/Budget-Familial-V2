from core.database import connexion


def transaction_existe(date, compte, montant, contrepartie):
    """
    Vérifie si une transaction existe déjà.
    """

    conn = connexion()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM transactions
        WHERE date=?
          AND compte=?
          AND montant=?
          AND contrepartie=?
        """,
        (
            date,
            compte,
            montant,
            contrepartie
        )
    )

    existe = cur.fetchone()[0] > 0

    conn.close()

    return existe


def ajouter_transaction(transaction):
    """
    Ajoute une transaction.
    """

    conn = connexion()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO transactions(

            date,
            compte,
            contrepartie,
            montant,

            categorie,
            sous_categorie,

            libelle,
            communication

        )

        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            str(transaction["Date"]),
            transaction["Compte"],
            transaction["Contrepartie"],
            float(transaction["Montant"]),

            transaction["Catégorie"],
            transaction["Sous-catégorie"],

            transaction["Libellé"],
            transaction["Communication"]
        )
    )

    conn.commit()
    conn.close()


def importer_transactions(df):
    """
    Importe toutes les transactions dans SQLite.
    """

    ajoutees = 0
    ignorees = 0

    for _, transaction in df.iterrows():

        existe = transaction_existe(
            str(transaction["Date"]),
            transaction["Compte"],
            float(transaction["Montant"]),
            transaction["Contrepartie"]
        )

        if existe:
            ignorees += 1
            continue

        ajouter_transaction(transaction)
        ajoutees += 1

    return ajoutees, ignorees