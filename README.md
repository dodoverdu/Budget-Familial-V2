# 💰 Budget Familial V2

Application personnelle de gestion financière développée en Python avec Streamlit.

L'objectif est de centraliser les relevés Belfius, catégoriser automatiquement les dépenses et disposer d'un véritable tableau de bord financier.

---

# Fonctionnalités actuelles

## ✅ Import Belfius

- Import de plusieurs fichiers CSV Belfius
- Fusion automatique des comptes
- Conversion des dates
- Conversion des montants
- Remplacement des IBAN par des noms compréhensibles

---

## ✅ Tableau de bord

- Patrimoine actuel
- Total des recettes
- Total des dépenses
- Situation bancaire
- Dernières transactions

---

## ✅ Transactions

- Recherche
- Filtre par compte
- Filtre par catégorie
- Filtre "À classer"

---

## ✅ Catégorisation

Les règles sont stockées dans :

data/categories.csv

Chaque nouvelle règle est automatiquement appliquée lors du prochain chargement.

---

# Structure du projet

```
Budget-Familial-V2/

app.py

belfius.py
categorisation.py
config.py

pages/
    Transactions.py
    Regles.py

data/
    categories.csv
    csv/

README.md
```

---

# Installation

Créer un environnement Python.

Installer les dépendances.

```bash
pip install pandas streamlit
```

---

# Lancement

```bash
streamlit run app.py
```

---

# Git

Voir les modifications

```bash
git status
```

Ajouter les fichiers

```bash
git add .
```

Créer un commit

```bash
git commit -m "Description"
```

Envoyer sur GitHub

```bash
git push
```

---

# Roadmap

## Version 0.5

- [ ] Gestion des règles améliorée
- [ ] Édition des transactions
- [ ] Assistant de catégorisation

## Version 0.6

- [ ] Budgets
- [ ] Statistiques
- [ ] Graphiques

## Version 0.7

- [ ] Intelligence financière
- [ ] Comparaison mensuelle
- [ ] Prévisions

## Version 1.0

- [ ] Gestion complète des finances familiales
- [ ] Import automatique
- [ ] Base SQLite
- [ ] Sauvegardes
- [ ] Export Excel

---

# Auteur

Donald Verdussen

Projet développé progressivement avec ChatGPT.
