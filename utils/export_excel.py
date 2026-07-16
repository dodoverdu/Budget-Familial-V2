from io import BytesIO
import pandas as pd


def exporter_transactions(df):

    sortie = BytesIO()

    with pd.ExcelWriter(
        sortie,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Transactions"
        )

    sortie.seek(0)

    return sortie