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
from gestion_fournisseur_a_regler import GestionFournisseurARegler
from utils.backup import backup_database
from ui.restore_dialog import RestoreDialog
from ui.synthese_interface import SyntheseDialog
from ui.aide_dialog import AideDialog
from ui.about_dialog import AboutDialog
from ui.email_config_dialog import EmailConfigDialog
from ui.company_config_dialog import CompanyConfigDialog
from company_config import COMPANY, get_logo_path
from version import APP_VERSION, APP_NAME


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator(self.db_manager)

        self.setWindowTitle(f"{APP_NAME} — v{APP_VERSION}")

        self.load_periode()
        self._connect_buttons()

        self._logo_loaded = False
        self.ui.labellogo.installEventFilter(self)
        self.ui.actionContacts.triggered.connect(self.open_contacts_manager)

        from PySide6.QtGui import QAction
        self.action_synthese = QAction("Synthèse...", self)
        self.action_synthese.triggered.connect(self.open_synthese)
        self.ui.menuConfig.addAction(self.action_synthese)

        self.action_restaurer = QAction("Restaurer une sauvegarde...", self)
        self.action_restaurer.triggered.connect(self.open_restore_dialog)
        self.ui.menuConfig.addAction(self.action_restaurer)

        self.action_email_config = QAction("Configuration email...", self)
        self.action_email_config.triggered.connect(self.open_email_config)
        self.ui.menuConfig.addSeparator()
        self.ui.menuConfig.addAction(self.action_email_config)

        self.action_company_config = QAction("Entreprise...", self)
        self.action_company_config.triggered.connect(self.open_company_config)
        self.ui.menuConfig.addAction(self.action_company_config)

        action_aide = QAction("Guide d'utilisation", self)
        action_aide.setShortcut("F1")
        action_aide.triggered.connect(self.open_aide)
        self.ui.menuAide.addAction(action_aide)

        action_about = QAction(f"À propos de {APP_NAME}...", self)
        action_about.triggered.connect(self.open_about)
        self.ui.menuAide.addSeparator()
        self.ui.menuAide.addAction(action_about)

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
            pixmap = QPixmap(get_logo_path())
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
            pdf_filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder le PDF",
                f"donnees_fiscales_{mois}_{annee}.pdf",
                "PDF Files (*.pdf);;All Files (*)"
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

    def open_synthese(self):
        dialog = SyntheseDialog(self)
        dialog.exec()

    def open_restore_dialog(self):
        dialog = RestoreDialog(self)
        dialog.exec()

    def open_gestion_fournisseur(self):
        self.gestion_fournisseur_window = GestionFournisseurARegler()
        self.gestion_fournisseur_window.exec()

    def open_aide(self):
        dialog = AideDialog(self)
        dialog.exec()

    def open_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def open_email_config(self):
        dialog = EmailConfigDialog(self)
        dialog.exec()

    def open_company_config(self):
        dialog = CompanyConfigDialog(self)
        if dialog.exec():
            self.setWindowTitle(f"{APP_NAME} — v{APP_VERSION}")
            self._logo_loaded = False
            self.load_logo()
