import os
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QEvent
from ui.ui_main_window import Ui_MainWindow
from database import DatabaseManager
from ui.depenses_interface import GestionDepenses
from ui.recettes_interface import GestionRecettes
from ui.contacts_interface import ContactsManager
from constants import DB_CONFIG, ERROR_MESSAGES, UI_CONFIG
from util import convert_month_to_number
from pdf_generator import PDFGenerator
from gestion_forniseur_a_regler import GestionFournisseurARegler
from utils.backup import backup_database
from ui.restore_dialog import RestoreDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator(self.db_manager)

        self.load_periode()
        self._connect_buttons()

        self._logo_loaded = False
        self.ui.labellogo.installEventFilter(self)
        self.ui.actionContacts.triggered.connect(self.open_contacts_manager)

        from PySide6.QtGui import QAction
        self.action_restaurer = QAction("Restaurer une sauvegarde...", self)
        self.action_restaurer.triggered.connect(self.open_restore_dialog)
        self.ui.menuConfig.addAction(self.action_restaurer)

    def eventFilter(self, obj, event):
        if obj == self.ui.labellogo and event.type() == QEvent.Show and not self._logo_loaded:
            self.load_logo()
            self._logo_loaded = True
        return super().eventFilter(obj, event)

    def _connect_buttons(self):
        button_connections = {
            "depensesButton": self.on_depenses_clicked,
            "recettesButton": self.on_recettes_clicked,
            "quitterButton": self.close,
            "pushButton_export_pdf": self.on_export_pdf_clicked,
            "pusharegeler": self.open_gestion_fournisseur,
        }
        for button_name, callback in button_connections.items():
            if hasattr(self.ui, button_name):
                getattr(self.ui, button_name).clicked.connect(callback)
            else:
                print(f"Erreur : Le bouton '{button_name}' n'existe pas dans le fichier .ui.")

    def load_logo(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "..", "data", "Logo.jpg")
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise FileNotFoundError(f"Impossible de charger l'image à {image_path}")
            self.ui.labellogo.setPixmap(pixmap)
            self.ui.labellogo.setScaledContents(True)
        except Exception as e:
            QMessageBox.warning(self, "Attention", f"Impossible de charger le logo : {str(e)}")

    def load_periode(self):
        try:
            mois, annee = self.db_manager.load_periode()
            self.ui.moisComboBox.setCurrentText(str(mois))
            self.ui.anneeLineEdit.setText(str(annee))
        except Exception as e:
            QMessageBox.warning(self, "Attention", f"Erreur lors du chargement de la période : {str(e)}")

    def save_periode(self):
        mois = self.ui.moisComboBox.currentText()
        annee = self.ui.anneeLineEdit.text()
        if not annee.isdigit():
            QMessageBox.warning(self, "Attention", "L'année doit être un nombre.")
            return
        try:
            self.db_manager.save_periode(mois, annee)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde de la période : {str(e)}")

    def closeEvent(self, event):
        self.save_periode()
        backup_database()
        event.accept()

    def on_export_pdf_clicked(self):
        try:
            self.save_periode()
            self.generate_ddf()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def generate_ddf(self):
        try:
            mois, annee = self.db_manager.load_periode()
            mois_numerique = convert_month_to_number(mois)
            options = QFileDialog.Options()
            pdf_filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder le PDF",
                f"donnees_fiscales_{mois}_{annee}.pdf",
                "PDF Files (*.pdf);;All Files (*)", options=options
            )
            if pdf_filename:
                self.pdf_generator.generate_ddf(mois_numerique, annee, pdf_filename)
                QMessageBox.information(self, "Succès", f"Le fichier PDF a été généré avec succès : {pdf_filename}")
        except Exception as e:
            QMessageBox.warning(self, "Attention", str(e))

    def on_depenses_clicked(self):
        try:
            self.save_periode()
            self.gestion_depenses_window = GestionDepenses()
            self.gestion_depenses_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture de la fenêtre des dépenses : {str(e)}")

    def on_recettes_clicked(self):
        try:
            self.save_periode()
            self.gestion_recettes_window = GestionRecettes()
            self.gestion_recettes_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture de la fenêtre des recettes : {str(e)}")

    def open_contacts_manager(self):
        self.contacts_manager = ContactsManager()
        self.contacts_manager.show()

    def open_restore_dialog(self):
        dialog = RestoreDialog(self)
        dialog.exec()

    def open_gestion_fournisseur(self):
        self.gestion_fournisseur_window = GestionFournisseurARegler()
        self.gestion_fournisseur_window.exec()
