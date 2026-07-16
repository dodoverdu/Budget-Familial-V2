from core.belfius import lire_transactions
from core.categorisation import categoriser
from core.database import creer_base
from core.importeur import importer_transactions

creer_base()

transactions = lire_transactions()
transactions = categoriser(transactions)

ajoutees, ignorees = importer_transactions(transactions)

print()
print("===================================")
print(f"Ajoutées : {ajoutees}")
print(f"Ignorées : {ignorees}")
print("===================================")