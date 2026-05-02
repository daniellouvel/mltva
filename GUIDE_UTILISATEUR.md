# MLTVA — Guide Utilisateur

## Table des matières

1. [Lancement de l'application](#1-lancement)
2. [Fenêtre principale](#2-fenêtre-principale)
3. [Gestion des Dépenses](#3-gestion-des-dépenses)
4. [Gestion des Recettes](#4-gestion-des-recettes)
5. [Calculette TVA](#5-calculette-tva)
6. [Contacts et Fournisseurs](#6-contacts-et-fournisseurs)
7. [Synthèse comptable](#7-synthèse-comptable)
8. [Export PDF](#8-export-pdf)
9. [Sauvegardes et Restauration](#9-sauvegardes-et-restauration)

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

## 4. Gestion des Recettes

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

## 5. Calculette TVA

La calculette est accessible dans les fenêtres Dépenses et Recettes via le bouton `Calculette TTC`.

**Utilisation (calcul inverse) :**

1. Saisir le **montant de TVA** dans le champ `Montant`
2. Sélectionner le **taux TVA** correspondant
3. Cliquer sur `Calculette TTC`

Le champ `Montant` se remplit automatiquement avec le **montant TTC**, et le champ `Montant TVA` affiche la TVA confirmée.

> **Exemple :** TVA = 20 €, taux = 20% → TTC calculé = 120 €, HT = 100 €

---

## 6. Contacts et Fournisseurs

Accessible via le menu **Config → Contacts**.

Permet de gérer le carnet d'adresses partagé entre clients (recettes) et fournisseurs (dépenses) :

- **Ajouter** un contact (nom, prénom, téléphone, email)
- **Modifier** les informations d'un contact existant
- **Supprimer** un contact

Lors de la saisie d'une dépense ou recette, si le fournisseur/client n'existe pas encore, l'application propose de l'ajouter automatiquement au carnet.

---

## 7. Synthèse comptable

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

## 8. Export PDF

1. Sélectionner la période (mois + année) dans la fenêtre principale
2. Cliquer sur `Export PDF`
3. Choisir l'emplacement et le nom du fichier
4. Le PDF est généré avec les dépenses, recettes et totaux de la période

---

## 9. Sauvegardes et Restauration

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
