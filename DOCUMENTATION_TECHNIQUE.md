# MLTVA — Documentation Technique

## Table des matières

1. [Architecture générale](#1-architecture-générale)
2. [Structure des fichiers](#2-structure-des-fichiers)
3. [Base de données](#3-base-de-données)
4. [Modules principaux](#4-modules-principaux)
5. [Interface graphique (UI)](#5-interface-graphique-ui)
6. [Système de sauvegarde](#6-système-de-sauvegarde)
7. [Compilation et distribution](#7-compilation-et-distribution)
8. [Dépendances](#8-dépendances)
9. [Ajouter une fonctionnalité](#9-ajouter-une-fonctionnalité)

---

## 1. Architecture générale

```
main.py
  └── charge le thème QSS
  └── affiche le splash screen
  └── instancie MainWindow
        ├── DatabaseManager (singleton)
        ├── PDFGenerator
        ├── GestionDepenses (QDialog)
        ├── GestionRecettes (QDialog)
        ├── ContactsManager (QMainWindow)
        ├── SyntheseDialog (QDialog)
        └── RestoreDialog (QDialog)
```

L'application suit un modèle simple **sans séparation MVC stricte** : chaque fenêtre accède directement à `DatabaseManager` pour lire et écrire les données.

**Singleton DatabaseManager** : une seule connexion SQLite est partagée entre toutes les fenêtres via le pattern singleton (`__new__`). La connexion est en mode WAL (Write-Ahead Logging) pour les performances.

---

## 2. Structure des fichiers

```
mltva/
├── main.py                        # Point d'entrée, chargement du thème
├── lancer.bat                     # Lancement développement
├── build_nuitka.bat               # Script de compilation exécutable
├── requirements.txt               # PySide6, reportlab
├── constants.py                   # DB_CONFIG, UI_CONFIG, ERROR_MESSAGES
├── util.py                        # Fonctions utilitaires partagées
├── database.py                    # DatabaseManager (singleton SQLite)
├── calculette.py                  # CalculetteDialog (fenêtre calculette)
├── pdf_generator.py               # PDFGenerator (ReportLab)
├── gestion_forniseur_a_regler.py  # Fenêtre fournisseurs à régler
│
├── ui/
│   ├── style.qss                  # Thème visuel (Qt Style Sheets)
│   ├── main_window.py             # MainWindow (fenêtre principale)
│   ├── base_gestion.py            # GestionBase (classe mère commune)
│   ├── depenses_interface.py      # GestionDepenses (+ bouton scan)
│   ├── recettes_interface.py      # GestionRecettes
│   ├── contacts_interface.py      # ContactsManager
│   ├── synthese_interface.py      # SyntheseDialog
│   ├── restore_dialog.py          # RestoreDialog
│   ├── aide_dialog.py             # AideDialog (fenêtre d'aide)
│   ├── async_worker.py            # Helpers threading (run_with_progress)
│   ├── scan_batch_dialog.py       # Mode séquentiel (facture par facture)
│   ├── scan_batch_table_dialog.py # Mode tableau (toutes factures à la fois)
│   ├── ui_main_window.py          # Généré Qt Designer — fenêtre principale
│   ├── ui_gestion_depenses.py     # Layout dépenses (réécrit en pur Python)
│   ├── ui_gestion_Recettes.py     # Layout recettes (réécrit en pur Python)
│   ├── ui_calculette.py           # Layout calculette
│   ├── ui_contacts_manager.py     # Layout contacts
│   └── ui_gestion_forniseur_a_regler.py
│
└── utils/
    └── backup.py                  # Système de sauvegarde automatique

data/
├── mlbdd.db                       # Base de données SQLite principale
├── Logo.jpg                       # Logo affiché au démarrage
└── backups/                       # Sauvegardes automatiques
    ├── mlbdd_AAAA-MM-JJ.db        # Journalières (10 max)
    ├── mlbdd_AAAA-MM.db           # Mensuelles (12 max)
    └── mlbdd_AAAA.db              # Annuelles
```

---

## 3. Base de données

**Fichier :** `data/mlbdd.db` (SQLite 3)

### Table `depenses`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER PK | Identifiant auto-incrémenté |
| `date` | TEXT | Format `AAAA-MM-JJ` (stockage ISO) |
| `fournisseur` | TEXT | Nom du fournisseur |
| `ttc` | REAL | Montant TTC |
| `tva_id` | REAL | Taux de TVA (ex: 20.0) |
| `montant_tva` | REAL | Montant de la TVA |
| `validation` | TEXT | `"Oui"` ou `"Non"` |
| `commentaire` | TEXT | Texte libre |

> **Note (v2.0) :** les insertions/updates sont maintenant effectuées dans une transaction atomique pour éviter les incohérences (voir `insert_depense_with_fournisseur`).

### Table `recettes`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER PK | Identifiant auto-incrémenté |
| `date` | TEXT | Format `AAAA-MM-JJ` |
| `client` | TEXT | Nom du client |
| `paiement` | TEXT | `"chèque"`, `"virement"` ou `"null"` |
| `numero_facture` | TEXT | Numéro de facture |
| `montant` | REAL | Montant TTC |
| `tva` | REAL | Taux de TVA |
| `montant_tva` | REAL | Montant de la TVA |
| `commentaire` | TEXT | Texte libre |

### Table `contacts`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER PK | Identifiant auto-incrémenté |
| `nom` | TEXT | Nom (clé de recherche) |
| `prenom` | TEXT | Prénom (optionnel) |
| `telephone` | TEXT | Téléphone (optionnel) |
| `email` | TEXT | Email (optionnel) |

> Les clients et fournisseurs partagent la même table `contacts`.

### Table `periode`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Toujours 1 (ligne unique) |
| `mois` | TEXT | Ex: `"Janvier"` |
| `annee` | TEXT | Ex: `"2026"` |

### Requêtes clés

```sql
-- Dépenses d'un mois
SELECT * FROM depenses
WHERE strftime('%m', date) = '05' AND strftime('%Y', date) = '2026';

-- Totaux mensuels pour la synthèse
SELECT COALESCE(SUM(ttc), 0), COALESCE(SUM(montant_tva), 0)
FROM depenses
WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?;
```

---

## 4. Modules principaux

### `database.py` — DatabaseManager

Singleton gérant toutes les interactions SQLite.

```python
db = DatabaseManager("data/mlbdd.db")  # Retourne toujours la même instance

# Lecture
rows = db.fetch_all(query, params)   # Retourne une liste de sqlite3.Row
row  = db.fetch_one(query, params)   # Retourne une sqlite3.Row ou None

# Écriture
db.execute_query(query, params)      # INSERT / UPDATE / DELETE → bool

# Méthodes métier
db.insert_depense(date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)
db.update_depense(id, ...)
db.delete_depense(id)

db.insert_recette(date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire)
db.update_recette(recette_id, ...)
db.delete_recette(recette_id)

db.contact_exists(nom)               # → bool (unifie fournisseur_exists + client_exists)
db.insert_fournisseur(nom)
db.insert_client(nom, prenom, telephone, email)
db.get_contact_id(nom)               # → int | None

# Scan / Import batch (v2.0)
db.insert_depense_with_fournisseur(date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire)
# → insère le fournisseur (si absent) et la dépense en transaction atomique

db.find_depense_doublons(ttc, fournisseur, mois, annee)
# → retourne une liste de doublon détectés (même TTC + fournisseur + mois/année)
```

**PRAGMA SQLite activés :**
- `synchronous = NORMAL` — performances améliorées
- `journal_mode = WAL` — lectures concurrentes
- `cache_size = -2000` — 2 Mo de cache

### `util.py` — Utilitaires

```python
convert_month_to_number("Janvier")  # → 1
calculate_tva("100", "20%")         # → 20.0
validate_fields(*args)              # → bool (True si tous non vides)
configure_fournisseur_combobox(combo, db_manager)  # Remplit un QComboBox
handle_exception(e, message)        # Affiche une QMessageBox d'erreur

class PeriodeManager:
    def get_periode()               # → (mois: str, annee: str)
```

### `constants.py` — Configuration

```python
DB_CONFIG = {
    "DEFAULT_PATH": "data/mlbdd.db",
    "DEFAULT_MONTH": "Janvier",
    "DEFAULT_YEAR": "2025",
}

UI_CONFIG = {
    "DEFAULT_TVA_RATES": ["0%", "5,5%", "10%", "20%"],
    "CALENDAR_VISIBLE": False,
}

ERROR_MESSAGES = {
    "DB_CONNECTION": "Connexion à la base de données établie.",
    "MISSING_FIELDS": "Veuillez remplir tous les champs obligatoires.",
    "ADD_SUCCESS": "La dépense a été ajoutée avec succès.",
    ...
}
```

### `pdf_generator.py` — PDFGenerator

Génère un document PDF avec ReportLab contenant :
- Les dépenses du mois sélectionné
- Les recettes du mois sélectionné
- Les totaux TTC et TVA

```python
pdf = PDFGenerator(db_manager)
pdf.generate_ddf(mois_numerique, annee, "chemin/fichier.pdf")
```

### `ui/async_worker.py` — Threading helpers

Exécute une fonction bloquante (OCR, IMAP, etc.) dans un `QThread` tout en affichant une barre de progression modale. Empêche le gel de l'UI.

```python
from ui.async_worker import run_with_progress, WorkerResult

result = run_with_progress(
    parent=self,
    title="Scan OCR",
    message="Analyse de 5 factures ...",
    target=_scan_all,
    args=(file_paths, selected_month, selected_year),
    cancellable=False
)

if result.success:
    print(result.value)  # Résultat de _scan_all
else:
    print(result.error)  # Exception levée
```

**`WorkerResult` :**
- `success: bool` — True si l'exécution a réussi
- `value: Any` — Résultat retourné par `target()`
- `error: BaseException` — Exception levée (si success=False)

### `ui/scan_batch_dialog.py` et `ui/scan_batch_table_dialog.py` — Scan batch

Deux modes de scanning de factures PDF en lot :

| Mode | Fichier | Description |
|------|---------|-------------|
| **Séquentiel** | `ScanBatchDialog` | Traite une facture à la fois, formulaire interactif avec correction manuelle possible |
| **Tableau** | `ScanBatchTableDialog` | Scanne toutes les factures en parallèle, affiche résultats dans tableau éditable avec checkboxes |

Chaque mode utilise `run_with_progress()` pour ne pas geler l'UI lors de l'OCR Tesseract.

**Mode Tableau (nouveau v2.0) :**
- Scanne tous les fichiers en `QThread`
- Affiche un tableau avec colonnes : Fichier, Date, Fournisseur, TTC, Taux TVA, Montant TVA, Validation, Commentaire
- Colonnes éditables pour correction avant enregistrement
- Checkboxes pour sélection des lignes à enregistrer
- Recalcul automatique du Montant TVA si TTC ou taux change
- Lignes en erreur affichées en rouge
- Détection de doublons lors de l'enregistrement

**Mode Séquentiel (hérité) :**
- Traite facture par facture
- Formulaire de saisie pour chaque facture
- Boutons : Valider, Passer, Arrêter
- Dialogue de confirmation pour dates hors période
- Résumé final avec compteurs

---

## 5. Interface graphique (UI)

### Hiérarchie des classes

```
QDialog
  └── GestionBase          (ui/base_gestion.py)
        ├── GestionDepenses (ui/depenses_interface.py)
        └── GestionRecettes (ui/recettes_interface.py)

QMainWindow
  └── MainWindow           (ui/main_window.py)

QDialog
  ├── SyntheseDialog       (ui/synthese_interface.py)
  ├── RestoreDialog        (ui/restore_dialog.py)
  └── CalculetteDialog     (calculette.py)

QMainWindow
  └── ContactsManager      (ui/contacts_interface.py)
```

### GestionBase — méthodes communes

| Méthode | Description |
|---------|-------------|
| `eventFilter` | Valider avec Entrée sauf sur quitter/tableau |
| `keyPressEvent` | Idem pour la touche Entrée globale |
| `show_calendar_on_focus` | Affiche le calendrier sur clic date |
| `on_calendar_date_clicked` | Remplit la date et cache le calendrier |
| `calculate_tva` | Calcule TVA depuis montant + taux |
| `calculate_and_update` | Calcul inverse TVA → TTC (calculette) |

### Fichiers de layout (ui_*.py)

Les fichiers `ui/ui_gestion_depenses.py` et `ui/ui_gestion_Recettes.py` sont écrits en **pur Python** avec des layouts dynamiques (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`) au lieu du positionnement absolu généré par Qt Designer.

Structure de chaque layout :
```
QVBoxLayout (main_layout)
  ├── QHBoxLayout (header)       ← titre + mois + année
  ├── QHBoxLayout (middle)       ← formulaire + calendrier
  ├── QHBoxLayout (btn_layout)   ← boutons d'action
  ├── QTableWidget               ← tableau (stretch=1)
  └── QHBoxLayout (footer)       ← totaux + supprimer + quitter
```

### Thème visuel (ui/style.qss)

Le fichier `ui/style.qss` est chargé au démarrage dans `main.py` via `app.setStyleSheet()`. Il s'applique à toute l'application.

**Palette de couleurs :**

| Rôle | Couleur |
|------|---------|
| Fond général | `#F0F4F8` (gris très clair) |
| Bleu principal | `#2C5F8A` |
| Bleu clair | `#4A90D9` |
| Vert (Valider) | `#27AE60` |
| Rouge (Supprimer) | `#E74C3C` |
| Orange (Effacer) | `#E67E22` |
| Violet (Calculette) | `#8E44AD` |
| Texte tableau | `#000000` |

Pour modifier le thème : éditer `ui/style.qss` — les changements sont pris en compte au prochain démarrage.

---

## 6. Système de sauvegarde

**Fichier :** `utils/backup.py`

La fonction `backup_database()` est appelée dans `MainWindow.closeEvent()`.

```python
def backup_database():
    today = datetime.now()
    _do_daily(today)    # mlbdd_AAAA-MM-JJ.db  (10 max, supprime les plus anciens)
    _do_monthly(today)  # mlbdd_AAAA-MM.db      (12 max)
    _do_annual(today)   # mlbdd_AAAA.db         (pas de limite)
```

**Constantes configurables dans `backup.py` :**
```python
DB_SOURCE  = "data/mlbdd.db"
BACKUP_DIR = "data/backups"
MAX_DAILY  = 10
MAX_MONTHLY = 12
```

**Restauration (`ui/restore_dialog.py`) :**
1. Liste les fichiers dans `data/backups/` par catégorie
2. Avant restauration, crée une sauvegarde de sécurité de la base actuelle
3. Copie le fichier sélectionné vers `data/mlbdd.db`

---

## 7. Compilation et distribution

### Prérequis

- Python 3.13 dans le venv
- Nuitka installé (`pip install nuitka`)
- Compilateur C (MinGW — Nuitka le propose automatiquement au premier lancement)

### Lancer la compilation

```bat
build_nuitka.bat
```

Durée : 20–30 minutes (première fois), plus rapide ensuite grâce au cache Nuitka.

### Options Nuitka utilisées

| Option | Rôle |
|--------|------|
| `--standalone` | Embarque Python et toutes les dépendances |
| `--enable-plugin=pyside6` | Support complet de PySide6/Qt6 |
| `--windows-console-mode=disable` | Pas de console noire au lancement |
| `--include-data-files=...` | Copie les images statiques |
| `--include-package=reportlab` | Force l'inclusion de ReportLab |

### Résultat

```
dist/mltva/          ← dossier à distribuer (~116 Mo)
  mltva.exe
  data/
    mlbdd.db
    Logo.jpg
  PySide6/           ← Qt6 (17 Mo)
  python313.dll      ← runtime Python (6 Mo)
  ...
```

> **Note :** le fichier `ui/style.qss` n'est pas copié dans `dist/` — le style est intégré dans l'exécutable par Nuitka. Pour modifier le thème après compilation, il faut recompiler.

---

## 8. Dépendances

| Package | Version | Usage |
|---------|---------|-------|
| `PySide6` | ≥ 6.8 | Interface graphique Qt6 |
| `reportlab` | ≥ 4.0 | Génération de PDF |
| `nuitka` | ≥ 2.0 | Compilation (dev uniquement) |

Python standard library utilisée : `sqlite3`, `datetime`, `os`, `sys`, `shutil`, `glob`.

---

## 9. Ajouter une fonctionnalité

### Ajouter un champ en base de données

1. Modifier la table dans SQLite (ou via `initialize_db.py`)
2. Mettre à jour les méthodes `insert_*` et `update_*` dans `database.py`
3. Ajouter le widget dans le fichier `ui/ui_gestion_*.py`
4. Mettre à jour `_get_depense_data()` / `add_new_row()` dans l'interface

### Ajouter un taux de TVA

Dans `constants.py` :
```python
UI_CONFIG = {
    "DEFAULT_TVA_RATES": ["0%", "5,5%", "10%", "20%", "8,5%"],  # Format: "X.XX%"
}
```

**Important :** les taux doivent être au format `"X.XX%"` (avec points décimaux, pas virgules) car ils sont comparés directement dans les combobox Qt.

### Modifier le thème visuel

Éditer `ui/style.qss` — syntaxe identique au CSS, sélecteurs Qt.
Exemple pour changer la couleur du bouton Valider :
```css
QPushButton[objectName="pushButtonValider"] {
    background-color: #2ECC71;  /* nouveau vert */
}
```

### Ajouter une fenêtre

1. Créer `ui/ma_fenetre.py` héritant de `QDialog`
2. Créer `ui/ui_ma_fenetre.py` avec les layouts
3. Importer et instancier depuis `ui/main_window.py`
4. Ajouter un bouton ou une action de menu dans `ui/ui_main_window.py`
