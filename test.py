from belfius import lire_transactions, lire_soldes

transactions = lire_transactions()
soldes = lire_soldes()

print("----------------------------------")
print("Transactions :", len(transactions))
print()

print(soldes)

print()

print("Total des soldes :", soldes["Solde"].sum())
print("----------------------------------")