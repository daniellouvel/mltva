import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from ui.ui_contacts_manager import Ui_ContactsManager  # Importer la classe générée
from database import DatabaseManager  # Assurez-vous que ce fichier existe
from PySide6.QtCore import QEvent  # Ajoutez cette importation

class ContactsManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ContactsManager()  # Créer une instance de la classe UI
        self.ui.setupUi(self)  # Configurer l'interface
        self.db_manager = DatabaseManager()  # Initialiser la gestion de la base de données
        self._contacts_loaded = False

        # Connecter les signaux
        self.ui.add_button.clicked.connect(self.add_contact)
        self.ui.edit_button.clicked.connect(self.edit_contact)
        self.ui.delete_button.clicked.connect(self.delete_contact)
        self.ui.contacts_table.cellClicked.connect(self.fill_inputs)
        self.ui.pushButton_quitter.clicked.connect(self.close)  # Connecter le bouton Quitter

        # Installer un event filter pour charger les contacts uniquement quand la table devient visible
        self.ui.contacts_table.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Gère le chargement des contacts uniquement quand la table devient visible."""
        if obj == self.ui.contacts_table and event.type() == QEvent.Show and not self._contacts_loaded:
            self.load_contacts()
            self._contacts_loaded = True
        return super().eventFilter(obj, event)

    def load_contacts(self):
        """Charge les contacts dans la table."""
        contacts = self.db_manager.fetch_all("SELECT nom, prenom, telephone, email FROM contacts")
        self.ui.contacts_table.setRowCount(len(contacts))
        
        # Masquer l'en-tête vertical
        self.ui.contacts_table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(contacts):
            for column_index, item in enumerate(row_data):
                self.ui.contacts_table.setItem(row_index, column_index, QTableWidgetItem(str(item)))

    def fill_inputs(self, row, column):
        """Remplit les champs de saisie avec les valeurs du contact sélectionné."""
        self.ui.name_input.setText(self.ui.contacts_table.item(row, 0).text())  # Nom
        self.ui.prenom_input.setText(self.ui.contacts_table.item(row, 1).text())  # Prénom
        self.ui.telephone_input.setText(self.ui.contacts_table.item(row, 2).text())  # Téléphone
        self.ui.email_input.setText(self.ui.contacts_table.item(row, 3).text())  # Email

    def add_contact(self):
        """Ajoute un nouveau contact à la base de données."""
        nom = self.ui.name_input.text()
        prenom = self.ui.prenom_input.text()  # Prénom est facultatif
        telephone = self.ui.telephone_input.text()
        email = self.ui.email_input.text()

        if not nom:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire.")
            return

        # Insérer le contact dans la base de données
        success = self.db_manager.insert_client(nom, prenom, telephone, email)  # Assurez-vous que cette méthode existe
        if success:
            self.load_contacts()  # Recharger les contacts
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout du contact.")

    def edit_contact(self):
        """Modifie le contact sélectionné dans la table."""
        selected_row = self.ui.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un contact à modifier.")
            return

        nom = self.ui.name_input.text()
        prenom = self.ui.prenom_input.text()  # Prénom est facultatif
        telephone = self.ui.telephone_input.text()
        email = self.ui.email_input.text()

        if not nom:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire.")
            return

        # Récupérer l'ID du contact à modifier
        contact_id = self.db_manager.get_contact_id(self.ui.contacts_table.item(selected_row, 0).text())  # Supposons que le nom est unique

        # Mettre à jour le contact dans la base de données
        success = self.db_manager.update_contact(contact_id, nom, prenom, telephone, email)
        if success:
            # Supprimer le message de succès
            # QMessageBox.information(self, "Succès", "Contact modifié avec succès.")
            self.load_contacts()  # Recharger les contacts
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la modification du contact.")

    def delete_contact(self):
        """Supprime le contact sélectionné dans la table."""
        selected_row = self.ui.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un contact à supprimer.")
            return

        contact_name = self.ui.contacts_table.item(selected_row, 0).text()  # Supposons que le nom est dans la première colonne
        response = QMessageBox.question(self, "Confirmation", f"Êtes-vous sûr de vouloir supprimer le contact '{contact_name}' ?",
                                         QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            # Récupérer l'ID du contact à supprimer
            contact_id = self.db_manager.get_contact_id(contact_name)  # Vous devez avoir une méthode pour obtenir l'ID
            success = self.db_manager.delete_contact(contact_id)
            if success:
                # Supprimer le message de succès
                # QMessageBox.information(self, "Succès", "Contact supprimé avec succès.")
                self.load_contacts()  # Recharger les contacts
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression du contact.")

    def clear_inputs(self):
        """Efface les champs de saisie."""
        self.ui.name_input.clear()
        self.ui.prenom_input.clear()
        self.ui.telephone_input.clear()
        self.ui.email_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContactsManager()
    window.show()
    sys.exit(app.exec()) 