from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget, QTextBrowser,
    QPushButton, QListWidgetItem, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from company_config import COMPANY

SECTIONS = {
    "Démarrage": """
<h2>Démarrage</h2>
<h3>Lancer l'application</h3>
<p>Double-cliquer sur <b>mltva.exe</b> (version compilée) ou sur <b>lancer.bat</b> (mode développement).</p>
<p>Un logo s'affiche brièvement, puis la fenêtre principale apparaît.</p>

<h3>Sélectionner la période</h3>
<p>Avant toute saisie, choisir le <b>mois</b> dans la liste déroulante et saisir l'<b>année</b>.
Toutes les dépenses et recettes affichées correspondent à cette période.</p>

<h3>Boutons principaux</h3>
<ul>
  <li><b>Dépenses</b> — ouvre la fenêtre de saisie des dépenses</li>
  <li><b>Recettes</b> — ouvre la fenêtre de saisie des recettes</li>
  <li><b>Export PDF</b> — génère le document fiscal du mois</li>
  <li><b>À régler</b> — liste des fournisseurs à régler</li>
  <li><b>Quitter</b> — ferme et sauvegarde automatiquement</li>
</ul>
""",

    "Saisir une dépense": """
<h2>Saisir une dépense</h2>
<ol>
  <li>Cliquer sur <b>Dépenses</b> dans la fenêtre principale</li>
  <li>Remplir le formulaire :</li>
</ol>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
  <tr style="background:#2C5F8A; color:white;"><th>Champ</th><th>Description</th></tr>
  <tr><td><b>Date</b></td><td>Cliquer sur le champ pour ouvrir le calendrier, ou saisir au format JJ/MM/AAAA</td></tr>
  <tr><td><b>Fournisseur</b></td><td>Choisir dans la liste ou saisir un nouveau nom</td></tr>
  <tr><td><b>TTC</b></td><td>Montant toutes taxes comprises</td></tr>
  <tr><td><b>TVA</b></td><td>Taux applicable : 0%, 5,5%, 10% ou 20%</td></tr>
  <tr><td><b>Montant TVA</b></td><td>Calculé automatiquement (non modifiable)</td></tr>
  <tr><td><b>Commentaire</b></td><td>Texte libre (optionnel)</td></tr>
  <tr><td><b>Validation</b></td><td>Cocher si la dépense est payée/validée</td></tr>
</table>
<br>
<ol start="3">
  <li>Cliquer sur <b>Valider</b> ou appuyer sur <b>Entrée</b></li>
</ol>
<p style="background:#FFF3CD; padding:8px; border-radius:4px;">
⚠️ Si une dépense identique existe déjà (même fournisseur, même montant, même mois),
une fenêtre de confirmation s'affiche pour éviter les doublons.
</p>
""",

    "Modifier / Supprimer une dépense": """
<h2>Modifier une dépense</h2>
<ol>
  <li>Cliquer sur la ligne dans le tableau — le formulaire se remplit automatiquement</li>
  <li>Modifier les champs souhaités</li>
  <li>Cliquer sur <b>Modifier</b></li>
</ol>

<h2>Supprimer une dépense</h2>
<ol>
  <li>Cliquer sur la ligne dans le tableau</li>
  <li>Cliquer sur <b>Supprimer</b></li>
  <li>Confirmer dans la boîte de dialogue</li>
</ol>

<h2>Effacer le formulaire</h2>
<p>Cliquer sur <b>Effacer</b> pour vider tous les champs et désélectionner la ligne en cours.</p>
""",

    "Saisir une recette": """
<h2>Saisir une recette</h2>
<ol>
  <li>Cliquer sur <b>Recettes</b> dans la fenêtre principale</li>
  <li>Remplir le formulaire :</li>
</ol>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
  <tr style="background:#2C5F8A; color:white;"><th>Champ</th><th>Description</th></tr>
  <tr><td><b>Date</b></td><td>Format JJ/MM/AAAA ou via le calendrier</td></tr>
  <tr><td><b>Client</b></td><td>Choisir dans la liste ou saisir un nouveau nom</td></tr>
  <tr><td><b>Paiement</b></td><td>chèque, virement ou null</td></tr>
  <tr><td><b>N° Facture</b></td><td>Numéro de la facture (optionnel)</td></tr>
  <tr><td><b>Montant</b></td><td>Montant TTC de la recette</td></tr>
  <tr><td><b>TVA</b></td><td>Taux applicable</td></tr>
  <tr><td><b>Montant TVA</b></td><td>Calculé automatiquement</td></tr>
  <tr><td><b>Commentaire</b></td><td>Texte libre (optionnel)</td></tr>
</table>
<br>
<ol start="3">
  <li>Cliquer sur <b>Valider</b></li>
</ol>
""",

    "Calculette TVA": """
<h2>Calculette TVA (calcul inverse)</h2>
<p>La calculette permet de calculer le <b>montant TTC</b> à partir d'un montant de TVA connu.</p>

<h3>Utilisation</h3>
<ol>
  <li>Saisir le <b>montant de TVA</b> dans le champ <i>Montant</i></li>
  <li>Sélectionner le <b>taux TVA</b> correspondant</li>
  <li>Cliquer sur <b>Calculette TTC</b></li>
</ol>
<p>Le champ <i>Montant</i> affiche alors le <b>TTC calculé</b>, et le champ <i>Montant TVA</i> confirme la TVA.</p>

<h3>Exemple</h3>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
  <tr style="background:#2C5F8A; color:white;"><th>TVA saisie</th><th>Taux</th><th>HT calculé</th><th>TTC affiché</th></tr>
  <tr><td>20,00 €</td><td>20%</td><td>100,00 €</td><td>120,00 €</td></tr>
  <tr><td>5,50 €</td><td>5,5%</td><td>100,00 €</td><td>105,50 €</td></tr>
</table>
""",

    "Scan factures — mode tableau": """
<h2>Scan factures — mode tableau (global)</h2>
<p>Le mode tableau permet de scanner <b>plusieurs factures à la fois</b> et de les valider en lot.</p>

<h3>Procédure</h3>
<ol>
  <li>Cliquer sur <b>Scanner facture</b> dans la fenêtre Dépenses</li>
  <li>Sélectionner une ou plusieurs factures PDF</li>
  <li>Choisir <b>Tableau</b> dans la boîte de dialogue</li>
  <li>Les factures sont scannées en parallèle (barre de progression)</li>
  <li>Modifier les cellules si nécessaire</li>
  <li>Cocher les factures à enregistrer</li>
  <li>Cliquer sur <b>Enregistrer les lignes cochées</b></li>
</ol>

<h3>Fonctionnalités</h3>
<ul>
  <li>Tableau éditable : modifiez Date, Fournisseur, TTC, Taux TVA, Validation, Commentaire</li>
  <li>Le <b>Montant TVA</b> se recalcule automatiquement quand vous modifiez le TTC ou le taux</li>
  <li>Les factures en erreur de scan s'affichent en <span style="background:#FADBD8; padding:2px;">rouge</span> et seront ignorées</li>
  <li>Détection des doublons lors de l'enregistrement (même fournisseur + montant + mois)</li>
  <li>Résumé final indiquant les factures enregistrées, ignorées, en doublon</li>
</ul>

<h3>Quand utiliser ce mode</h3>
<p style="background:#D5F4E6; padding:8px; border-radius:4px;">
✓ Recommandé pour de nombreuses factures (10+) ou quand vous avez peu de corrections manuelles à faire.
</p>
""",

    "Scan factures — mode séquentiel": """
<h2>Scan factures — mode séquentiel (pas à pas)</h2>
<p>Le mode séquentiel traite <b>une facture à la fois</b> avec possibilité de correction interactive.</p>

<h3>Procédure</h3>
<ol>
  <li>Cliquer sur <b>Scanner facture</b> dans la fenêtre Dépenses</li>
  <li>Sélectionner une ou plusieurs factures PDF</li>
  <li>Choisir <b>Séquentiel</b> dans la boîte de dialogue</li>
  <li>Pour chaque facture :
    <ul>
      <li>L'OCR affiche les données détectées</li>
      <li>Modifier les champs si nécessaire</li>
      <li>Cliquer <b>Valider</b> pour enregistrer, <b>Passer</b> pour ignorer, ou <b>Arrêter</b> pour terminer</li>
    </ul>
  </li>
  <li>Un résumé final affiche le nombre de factures enregistrées</li>
</ol>

<h3>Dialogues spéciaux</h3>
<ul>
  <li><b>Période différente</b> — si la date de la facture ne correspond pas au mois actif, l'application propose d'ajuster automatiquement</li>
  <li><b>Doublon détecté</b> — confirmation avant d'ajouter une dépense identique</li>
</ul>

<h3>Quand utiliser ce mode</h3>
<p style="background:#FFF3CD; padding:8px; border-radius:4px;">
✓ Recommandé pour peu de factures (1-3) ou quand vous avez des corrections manuelles importantes à effectuer.
</p>
""",

    "Contacts et Fournisseurs": """
<h2>Contacts et Fournisseurs</h2>
<p>Accessible via le menu <b>Config → Contacts</b>.</p>
<p>Le carnet de contacts est partagé entre clients (recettes) et fournisseurs (dépenses).</p>

<h3>Ajouter un contact</h3>
<p>Remplir les champs Nom, Prénom, Téléphone, Email puis cliquer sur <b>Ajouter</b>.</p>

<h3>Modifier un contact</h3>
<p>Cliquer sur le contact dans la liste, modifier les champs, cliquer sur <b>Modifier</b>.</p>

<h3>Suppression</h3>
<p>Sélectionner le contact et cliquer sur <b>Supprimer</b>.</p>

<h3>Ajout automatique</h3>
<p>Lors de la saisie d'une dépense ou recette, si le fournisseur/client n'existe pas,
l'application propose de l'ajouter automatiquement.</p>
""",

    "Synthèse comptable": """
<h2>Synthèse comptable</h2>
<p>Accessible via le menu <b>Config → Synthèse</b>.</p>

<h3>Onglet Mensuel</h3>
<p>Affiche un résumé pour le mois actif :</p>
<ul>
  <li><span style="color:#C0392B;"><b>Dépenses</b></span> — Total TTC + TVA déductible</li>
  <li><span style="color:#27AE60;"><b>Recettes</b></span> — Total TTC + TVA collectée</li>
  <li><span style="color:#2C5F8A;"><b>Bilan</b></span> — Solde (Recettes − Dépenses) + TVA à reverser</li>
</ul>
<p>Les montants positifs s'affichent en <span style="color:green;"><b>vert</b></span>,
les négatifs en <span style="color:red;"><b>rouge</b></span>.</p>

<h3>Onglet Annuel</h3>
<p>Tableau des 12 mois avec pour chaque mois : TTC dépenses, TVA dépenses,
TTC recettes, TVA recettes, solde, TVA à reverser.</p>
<p>La dernière ligne affiche les <b>totaux annuels</b>.</p>
""",

    "Export PDF": """
<h2>Export PDF</h2>
<p>Génère un document fiscal pour la période sélectionnée.</p>

<h3>Procédure</h3>
<ol>
  <li>Sélectionner le <b>mois</b> et l'<b>année</b> dans la fenêtre principale</li>
  <li>Cliquer sur <b>Export PDF</b></li>
  <li>Choisir l'emplacement et le nom du fichier dans la boîte de dialogue</li>
  <li>Le PDF est généré avec les dépenses, recettes et totaux du mois</li>
</ol>
""",

    "Sauvegardes": """
<h2>Sauvegardes automatiques</h2>
<p>À chaque fermeture de l'application, trois sauvegardes sont créées dans <b>data/backups/</b> :</p>

<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; width:100%;">
  <tr style="background:#2C5F8A; color:white;"><th>Type</th><th>Nom du fichier</th><th>Conservées</th></tr>
  <tr><td>Journalière</td><td>mlbdd_2026-05-03.db</td><td>10 derniers jours</td></tr>
  <tr><td>Mensuelle</td><td>mlbdd_2026-05.db</td><td>12 derniers mois</td></tr>
  <tr><td>Annuelle</td><td>mlbdd_2026.db</td><td>Toutes conservées</td></tr>
</table>

<h2>Restaurer une sauvegarde</h2>
<ol>
  <li>Menu <b>Config → Restaurer une sauvegarde</b></li>
  <li>Choisir la sauvegarde dans la liste</li>
  <li>Cliquer sur <b>Restaurer</b></li>
  <li>Redémarrer l'application</li>
</ol>
<p style="background:#F8D7DA; padding:8px; border-radius:4px;">
⚠️ La restauration remplace toutes les données actuelles.
Une sauvegarde de sécurité est créée automatiquement avant la restauration.
</p>
""",
}


class AideDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Aide — {COMPANY['name']}")
        self.setMinimumSize(820, 560)
        self.setModal(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        splitter = QSplitter(Qt.Horizontal)

        self.liste = QListWidget()
        self.liste.setMaximumWidth(220)
        self.liste.setFont(QFont("Segoe UI", 10))
        for titre in SECTIONS:
            item = QListWidgetItem(titre)
            self.liste.addItem(item)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(False)

        splitter.addWidget(self.liste)
        splitter.addWidget(self.browser)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

        fermer = QPushButton("Fermer")
        fermer.setObjectName("quitterButton")
        fermer.clicked.connect(self.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(fermer)
        layout.addLayout(btn_layout)

        self.liste.currentRowChanged.connect(self._afficher_section)
        self.liste.setCurrentRow(0)

    def _afficher_section(self, index):
        if index < 0:
            return
        titre = self.liste.item(index).text()
        html = SECTIONS.get(titre, "")
        self.browser.setHtml(f"""
        <html><body style="font-family: Segoe UI; font-size: 10pt; color: #0D1B2A; padding: 8px;">
        {html}
        </body></html>
        """)
