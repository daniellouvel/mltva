from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QEvent, Qt
from ui.ui_contacts_manager import Ui_ContactsManager
from ui.aide_dialog import AideDialog
from database import DatabaseManager


class ContactsManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ContactsManager()
        self.ui.setupUi(self)
        self.db_manager = DatabaseManager()
        self._contacts_loaded = False

        self.ui.add_button.clicked.connect(self.add_contact)
        self.ui.edit_button.clicked.connect(self.edit_contact)
        self.ui.delete_button.clicked.connect(self.delete_contact)
        self.ui.contacts_table.cellClicked.connect(self.fill_inputs)
        self.ui.pushButton_quitter.clicked.connect(self.close)
        self.ui.contacts_table.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.ui.contacts_table and event.type() == QEvent.Show and not self._contacts_loaded:
            self.load_contacts()
            self._contacts_loaded = True
        return super().eventFilter(obj, event)

    def load_contacts(self):
        contacts = self.db_manager.fetch_all("SELECT nom, prenom, telephone, email FROM contacts")
        self.ui.contacts_table.setRowCount(len(contacts))
        self.ui.contacts_table.verticalHeader().setVisible(False)
        for row_index, row_data in enumerate(contacts):
            for column_index, item in enumerate(row_data):
                self.ui.contacts_table.setItem(row_index, column_index, QTableWidgetItem(str(item)))

    def fill_inputs(self, row, column):
        self.ui.name_input.setText(self.ui.contacts_table.item(row, 0).text())
        self.ui.prenom_input.setText(self.ui.contacts_table.item(row, 1).text())
        self.ui.telephone_input.setText(self.ui.contacts_table.item(row, 2).text())
        self.ui.email_input.setText(self.ui.contacts_table.item(row, 3).text())

    def add_contact(self):
        nom = self.ui.name_input.text()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire.")
            return
        success = self.db_manager.insert_client(
            nom,
            self.ui.prenom_input.text(),
            self.ui.telephone_input.text(),
            self.ui.email_input.text(),
        )
        if success:
            self.load_contacts()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de l'ajout du contact.")

    def edit_contact(self):
        selected_row = self.ui.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un contact à modifier.")
            return
        nom = self.ui.name_input.text()
        if not nom:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire.")
            return
        contact_id = self.db_manager.get_contact_id(self.ui.contacts_table.item(selected_row, 0).text())
        success = self.db_manager.update_contact(
            contact_id, nom,
            self.ui.prenom_input.text(),
            self.ui.telephone_input.text(),
            self.ui.email_input.text(),
        )
        if success:
            self.load_contacts()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la modification du contact.")

    def delete_contact(self):
        selected_row = self.ui.contacts_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un contact à supprimer.")
            return
        contact_name = self.ui.contacts_table.item(selected_row, 0).text()
        response = QMessageBox.question(self, "Confirmation",
                                        f"Êtes-vous sûr de vouloir supprimer le contact '{contact_name}' ?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            contact_id = self.db_manager.get_contact_id(contact_name)
            success = self.db_manager.delete_contact(contact_id)
            if success:
                self.load_contacts()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression du contact.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            AideDialog(self).exec()
        else:
            super().keyPressEvent(event)

    def clear_inputs(self):
        self.ui.name_input.clear()
        self.ui.prenom_input.clear()
        self.ui.telephone_input.clear()
        self.ui.email_input.clear()
