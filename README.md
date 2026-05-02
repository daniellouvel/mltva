# MLTVA — Gestion comptable TVA

Application de bureau pour la gestion des dépenses et recettes avec calcul automatique de la TVA, destinée aux auto-entrepreneurs et petites entreprises.

## Fonctionnalités

- **Dépenses** — saisie, modification, suppression avec calcul TVA, détection de doublons, confirmation avant suppression
- **Recettes** — saisie, modification, suppression avec calcul TVA
- **Contacts / Fournisseurs** — carnet de contacts et suivi des fournisseurs à régler
- **Calculette TVA** — calcul TTC à partir d'un montant TVA et d'un taux
- **Export PDF** — génération d'un document fiscal par période (mois/année)
- **Synthèse comptable** — vue mensuelle et annuelle (TTC dépenses/recettes, TVA, solde, TVA à reverser)
- **Sauvegarde automatique** — journalière, mensuelle et annuelle à la fermeture (dans `data/backups/`)
- **Restauration** — depuis n'importe quelle sauvegarde via le menu Config

## Technologies

- Python 3.13
- PySide6 (interface graphique Qt6)
- SQLite (base de données)
- ReportLab (génération PDF)
- Nuitka (compilation en exécutable Windows)

## Installation (mode développement)

### Prérequis

- Python 3.13

### Mise en place

```bash
# Créer l'environnement virtuel
python -m venv venv

# Installer les dépendances
venv\Scripts\pip install -r requirements.txt
```

## Lancement

Double-cliquer sur `lancer.bat` ou :

```bash
venv\Scripts\python.exe main.py
```

## Compilation en exécutable Windows

```bash
build_nuitka.bat
```

Génère `dist\mltva\mltva.exe` avec toutes les dépendances embarquées (~116 Mo).
Pour distribuer : copier le dossier `dist\mltva\` complet.

## Structure du projet

```
mltva/
├── main.py                      # Point d'entrée + chargement du thème
├── lancer.bat                   # Lancement rapide
├── build_nuitka.bat             # Compilation exécutable
├── database.py                  # Accès base de données SQLite
├── calculette.py                # Calculette TVA inverse
├── pdf_generator.py             # Génération des PDF fiscaux
├── util.py                      # Fonctions utilitaires
├── constants.py                 # Constantes de l'application
├── ui/
│   ├── style.qss                # Thème visuel (couleurs, boutons, tableau)
│   ├── main_window.py           # Fenêtre principale
│   ├── base_gestion.py          # Classe de base commune Dépenses/Recettes
│   ├── depenses_interface.py    # Fenêtre des dépenses
│   ├── recettes_interface.py    # Fenêtre des recettes
│   ├── contacts_interface.py    # Gestion des contacts
│   ├── synthese_interface.py    # Synthèse mensuelle et annuelle
│   ├── restore_dialog.py        # Restauration de sauvegarde
│   └── ui_*.py                  # Définitions d'interface Qt
├── utils/
│   └── backup.py                # Sauvegarde automatique (J/M/A)
├── data/
│   ├── mlbdd.db                 # Base de données SQLite
│   ├── Logo.jpg                 # Logo affiché au démarrage
│   └── backups/                 # Sauvegardes automatiques
└── requirements.txt
```

## Base de données

La base de données SQLite se trouve dans `data/mlbdd.db` et contient les tables :

| Table | Contenu |
|-------|---------|
| `depenses` | Dépenses par période (date, fournisseur, TTC, TVA, validation) |
| `recettes` | Recettes par période (date, client, paiement, facture, montant, TVA) |
| `contacts` | Carnet de contacts partagé clients/fournisseurs |
| `periode` | Période active (mois/année) |

## Sauvegardes

À chaque fermeture de l'application, trois sauvegardes sont créées automatiquement dans `data/backups/` :

- **Journalière** — `mlbdd_AAAA-MM-JJ.db` (10 dernières conservées)
- **Mensuelle** — `mlbdd_AAAA-MM.db` (12 dernières conservées)
- **Annuelle** — `mlbdd_AAAA.db`

Pour restaurer : menu **Config → Restaurer une sauvegarde**.
