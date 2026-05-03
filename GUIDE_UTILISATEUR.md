# MLTVA — Guide Utilisateur

## Table des matières

1. [Lancement de l'application](#1-lancement)
2. [Fenêtre principale](#2-fenêtre-principale)
3. [Gestion des Dépenses](#3-gestion-des-dépenses)
4. [Scan factures par lot](#4-scan-factures-par-lot)
5. [Gestion des Recettes](#5-gestion-des-recettes)
6. [Calculette TVA](#6-calculette-tva)
7. [Contacts et Fournisseurs](#7-contacts-et-fournisseurs)
8. [Synthèse comptable](#8-synthèse-comptable)
9. [Export PDF](#9-export-pdf)
10. [Sauvegardes et Restauration](#10-sauvegardes-et-restauration)
11. [Déploiement multi-entreprise](#11-déploiement-multi-entreprise)

---

## 1. Lancement

**Avec l'exécutable :** double-cliquer sur `mltva.exe` dans le dossier `dist\mltva\`.

**En mode développement :** double-cliquer sur `lancer.bat`.

Un logo s'affiche brièvement au démarrage, puis la fenêtre principale apparaît.

---

## 2. Fenêtre principale

![Fenêtre principale](data/Logo.jpg)

La fenêtre principale comporte :

- **Logo** de l'entreprise (en haut à gauche)
- **Sélection de la période** : choisir le mois (liste déroulante) et saisir l'année
- **Boutons de navigation** :
  - `Dépenses` — ouvre la fenêtre de saisie des dépenses
  - `Recettes` — ouvre la fenêtre de saisie des recettes
  - `Export PDF` — génère le document fiscal de la période
  - `À régler` — liste des fournisseurs à régler
  - `Quitter` — ferme l'application (déclenche la sauvegarde automatique)

> **Important :** sélectionner la bonne période avant d'ouvrir Dépenses ou Recettes. Les données affichées correspondent toujours au mois et à l'année sélectionnés.

---

## 3. Gestion des Dépenses

### Saisir une dépense

1. Cliquer sur `Dépenses` dans la fenêtre principale
2. Remplir les champs du formulaire :
   - **Date** — cliquer sur le champ pour afficher le calendrier, ou saisir au format `JJ/MM/AAAA`
   - **Fournisseur** — choisir dans la liste ou saisir un nouveau nom
   - **TTC** — montant toutes taxes comprises
   - **TVA** — sélectionner le taux (0%, 5,5%, 10%, 20%)
   - **Montant TVA** — calculé automatiquement (non modifiable)
   - **Commentaire** — texte libre (optionnel)
   - **Validation** — cocher si la dépense est validée/payée
3. Cliquer sur `Valider` ou appuyer sur `Entrée`

### Modifier une dépense

1. Cliquer sur la ligne dans le tableau — le formulaire se remplit automatiquement
2. Modifier les champs souhaités
3. Cliquer sur `Modifier`

### Supprimer une dépense

1. Cliquer sur la ligne dans le tableau
2. Cliquer sur `Supprimer`
3. Confirmer la suppression dans la boîte de dialogue

### Effacer le formulaire

Cliquer sur `Effacer` pour vider tous les champs et désélectionner la ligne.

### Détection de doublons

Si une dépense identique (même fournisseur, même montant, même mois) existe déjà, une fenêtre de confirmation s'affiche. Cela évite les saisies en double.

---

## 4. Scan factures par lot

### Accès

1. Dans la fenêtre **Dépenses**, cliquer sur le bouton `Scanner facture`
2. Sélectionner une ou plusieurs factures PDF
3. Choisir le mode de traitement

### Mode Tableau (global)

Le mode tableau scanne **toutes les factures simultanément** et affiche les résultats dans un tableau éditable :

1. Un OCR rapide analyse tous les fichiers en parallèle (avec barre de progression)
2. Les résultats s'affichent dans un tableau où vous pouvez :
   - **Modifier les cellules** : Date, Fournisseur, TTC, Taux TVA, Montaire TVA (auto-recalculée), Validation, Commentaire
   - **Cocher les lignes** à enregistrer (les cases à cocher permettent la sélection multiple)
   - **Valider en lot** : cliquer sur `Enregistrer les lignes cochées`

3. Les factures avec erreur de scan s'affichent en **rouge** et seront ignorées
4. Un résumé final indique combien de factures ont été enregistrées, ignorées, ou en doublon

**Avantage :** rapidité, aperçu global avant enregistrement, modification groupée facile.

### Mode Séquentiel

Le mode séquentiel traite **une facture à la fois** avec confirmation interactive :

1. Chaque facture est scannée individuellement
2. Un formulaire s'affiche avec les données détectées (modifiables)
3. Vous validez, passez, ou stoppez le traitement
4. Un résumé final affiche les résultats

**Avantage :** contrôle précis, interaction facture par facture, idéal pour les corrections manuelles.

### Choix du mode

À chaque scan, un dialogue vous demande de choisir :
- **Tableau** — traitement rapide et global (recommandé pour beaucoup de factures)
- **Séquentiel** — traitement détaillé et pas à pas (recommandé pour peu de factures ou corrections manuelles)

### Notes

- Les dates hors période sont automatiquement ajustées à la période active (ex: `01/05/2026`)
- La détection de TVA est automatique (20% par défaut)
- Les doublons sont détectés lors de l'enregistrement (même fournisseur + montant + mois)
- Vous pouvez toujours éditer manuellement les dépenses après enregistrement

---

## 5. Gestion des Recettes

### Saisir une recette

1. Cliquer sur `Recettes` dans la fenêtre principale
2. Remplir les champs :
   - **Date** — format `JJ/MM/AAAA` ou via le calendrier
   - **Client** — choisir dans la liste ou saisir un nouveau nom
   - **Paiement** — chèque, virement ou null
   - **N° Facture** — numéro de la facture (optionnel)
   - **Montant** — montant TTC de la recette
   - **TVA** — taux applicable
   - **Montant TVA** — calculé automatiquement
   - **Commentaire** — texte libre (optionnel)
3. Cliquer sur `Valider`

### Modifier / Supprimer

Même fonctionnement que pour les dépenses (cliquer sur la ligne, puis `Modifier` ou `Supprimer`).

---

## 6. Calculette TVA

La calculette est accessible dans les fenêtres Dépenses et Recettes via le bouton `Calculette TTC`.

**Utilisation (calcul inverse) :**

1. Saisir le **montant de TVA** dans le champ `Montant`
2. Sélectionner le **taux TVA** correspondant
3. Cliquer sur `Calculette TTC`

Le champ `Montant` se remplit automatiquement avec le **montant TTC**, et le champ `Montant TVA` affiche la TVA confirmée.

> **Exemple :** TVA = 20 €, taux = 20% → TTC calculé = 120 €, HT = 100 €

---

## 7. Contacts et Fournisseurs

Accessible via le menu **Config → Contacts**.

Permet de gérer le carnet d'adresses partagé entre clients (recettes) et fournisseurs (dépenses) :

- **Ajouter** un contact (nom, prénom, téléphone, email)
- **Modifier** les informations d'un contact existant
- **Supprimer** un contact

Lors de la saisie d'une dépense ou recette, si le fournisseur/client n'existe pas encore, l'application propose de l'ajouter automatiquement au carnet.

---

## 8. Synthèse comptable

Accessible via le menu **Config → Synthèse**.

### Onglet Mensuel

Affiche pour le mois en cours :

| Section | Données |
|---------|---------|
| **Dépenses** | Total TTC, TVA déductible |
| **Recettes** | Total TTC, TVA collectée |
| **Bilan** | Solde (Recettes − Dépenses), TVA à reverser |

Les montants positifs sont affichés en **vert**, les négatifs en **rouge**.

### Onglet Annuel

Tableau des 12 mois de l'année avec pour chaque mois :
- TTC Dépenses / TVA Dépenses
- TTC Recettes / TVA Recettes
- Solde mensuel
- TVA à reverser

La dernière ligne affiche les **totaux annuels**.

---

## 9. Export PDF

1. Sélectionner la période (mois + année) dans la fenêtre principale
2. Cliquer sur `Export PDF`
3. Choisir l'emplacement et le nom du fichier
4. Le PDF est généré avec les dépenses, recettes et totaux de la période

---

## 10. Sauvegardes et Restauration

### Sauvegardes automatiques

À chaque fermeture de l'application, trois sauvegardes sont créées dans `data/backups/` :

| Type | Nom du fichier | Nombre conservé |
|------|---------------|-----------------|
| Journalière | `mlbdd_2026-05-03.db` | 10 derniers jours |
| Mensuelle | `mlbdd_2026-05.db` | 12 derniers mois |
| Annuelle | `mlbdd_2026.db` | illimité |

### Restaurer une sauvegarde

1. Menu **Config → Restaurer une sauvegarde**
2. Choisir la sauvegarde dans la liste (Journalier / Mensuel / Annuel)
3. Cliquer sur `Restaurer`
4. Une sauvegarde de sécurité est créée automatiquement avant la restauration
5. Redémarrer l'application

> **Attention :** la restauration remplace toutes les données actuelles par celles de la sauvegarde choisie.

---

## 11. Déploiement multi-entreprise

L'application peut être configurée pour n'importe quelle entreprise sans modifier le code. Toute la personnalisation passe par un seul fichier : `company.json`.

### Fichier `company.json`

```json
{
  "name": "NomEntreprise",
  "legal": "NomEntreprise SARL",
  "logo": "data/Logo.jpg",
  "db_name": "mlbdd.db",
  "backup_dir": "data/backups"
}
```

| Champ | Description |
|-------|-------------|
| `name` | Nom affiché dans l'UI, les titres de fenêtres et le PDF |
| `legal` | Dénomination légale (affiché dans "À propos") |
| `logo` | Chemin relatif vers l'image du logo (JPG, PNG) |
| `db_name` | Nom du fichier de base de données (dans `data/`) |
| `backup_dir` | Dossier des sauvegardes automatiques |

### Procédure de déploiement

1. Copier le dossier complet de l'application vers le poste cible
2. Éditer `company.json` avec les informations de la nouvelle entreprise
3. Remplacer `data/Logo.jpg` par le logo de l'entreprise (même nom, ou mettre à jour `logo` dans le JSON)
4. Lancer l'application — toute l'interface (titres, splash, PDF, aide) utilise automatiquement le nouveau nom

> **Note :** si `company.json` est absent ou corrompu, l'application démarre avec les valeurs MLTVA par défaut.

### Version de l'application

La version courante est visible :
- Dans le titre de la fenêtre principale : `NomEntreprise — v2.0.0`
- Sur le splash screen au démarrage
- Dans le menu **Aide → À propos**

Pour mettre à jour la version lors d'une nouvelle release, modifier `version.py` :
```python
APP_VERSION = "2.1.0"
```
