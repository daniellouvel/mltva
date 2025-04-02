# -*- coding: utf-8 -*-
# main.py - Version 2.4

import sys
import os
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap
from ui.ui_main_window import Ui_MainWindow
from database import DatabaseManager
from gestion_depenses import GestionDepenses
from gestion_recettes import GestionRecettes
from constants import DB_CONFIG, ERROR_MESSAGES, UI_CONFIG
from util import convert_month_to_number
from pdf_generator import PDFGenerator
from contacts_manager import ContactsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialisation de la base de données via DatabaseManager
        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator(self.db_manager)

        # Charger les valeurs de la période
        self.load_periode()

        # Connexion des boutons
        self._connect_buttons()

        # Chargement du logo
        self.load_logo()

        # Connexion de l'action "Contacts"
        self.ui.actionContacts.triggered.connect(self.open_contacts_manager)

    def _connect_buttons(self):
        """Connecte tous les boutons de l'interface."""
        button_connections = {
            "depensesButton": self.on_depenses_clicked,
            "recettesButton": self.on_recettes_clicked,
            "quitterButton": self.close,
            "pushButton_export_pdf": self.on_export_pdf_clicked
        }

        for button_name, callback in button_connections.items():
            if hasattr(self.ui, button_name):
                getattr(self.ui, button_name).clicked.connect(callback)
            else:
                print(f"Erreur : Le bouton '{button_name}' n'existe pas dans le fichier .ui.")

    def load_logo(self):
        """Charge et affiche le logo dans le QLabel."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "data", "Logo.jpg")

            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise FileNotFoundError(f"Impossible de charger l'image à {image_path}")

            self.ui.labellogo.setPixmap(pixmap)
            self.ui.labellogo.setScaledContents(True)
        except Exception as e:
            QMessageBox.warning(self, "Attention", f"Impossible de charger le logo : {str(e)}")

    def load_periode(self):
        """Charge les valeurs de la table 'periode' et pré-remplit les widgets."""
        try:
            mois, annee = self.db_manager.load_periode()
            self.ui.moisComboBox.setCurrentText(str(mois))
            self.ui.anneeLineEdit.setText(str(annee))
        except Exception as e:
            QMessageBox.warning(self, "Attention", f"Erreur lors du chargement de la période : {str(e)}")

    def save_periode(self):
        """Sauvegarde les valeurs de mois et année dans la table 'periode'."""
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
        """Méthode appelée lors de la fermeture de la fenêtre."""
        self.save_periode()
        event.accept()

    def on_export_pdf_clicked(self):
        """Méthode appelée lorsque le bouton d'exportation PDF est cliqué."""
        try:
            self.save_periode()  # Sauvegarde de la période avant d'exporter le PDF
            self.generate_ddf()  # Appeler la méthode pour générer le PDF
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def generate_ddf(self):
        """Génère un fichier PDF contenant les données des dépenses et recettes de la période active."""
        try:
            # Récupérer la période active
            mois, annee = self.db_manager.load_periode()
            mois_numerique = convert_month_to_number(mois)

            # Ouvrir un dialogue de sauvegarde pour choisir l'emplacement du fichier PDF
            options = QFileDialog.Options()
            pdf_filename, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le PDF", f"donnees_fiscales_{mois}_{annee}.pdf", "PDF Files (*.pdf);;All Files (*)", options=options)

            if pdf_filename:  # Vérifiez si un nom de fichier a été sélectionné
                # Générer le PDF
                self.pdf_generator.generate_ddf(mois_numerique, annee, pdf_filename)
                QMessageBox.information(self, "Succès", f"Le fichier PDF a été généré avec succès : {pdf_filename}")
        except Exception as e:
            QMessageBox.warning(self, "Attention", str(e))

    def on_depenses_clicked(self):
        """Méthode appelée lorsque le bouton 'Dépense' est cliqué."""
        try:
            self.save_periode()  # Sauvegarde automatique avant d'ouvrir la fenêtre
            self.gestion_depenses_window = GestionDepenses()
            self.gestion_depenses_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture de la fenêtre des dépenses : {str(e)}")

    def on_recettes_clicked(self):
        """Méthode appelée lorsque le bouton 'Recettes' est cliqué."""
        try:
            self.save_periode()  # Sauvegarde automatique avant d'ouvrir la fenêtre
            self.gestion_recettes_window = GestionRecettes()
            self.gestion_recettes_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture de la fenêtre des recettes : {str(e)}")

    def open_contacts_manager(self):
        """Ouvre la fenêtre de gestion des contacts."""
        self.contacts_manager = ContactsManager()  # Créez une instance de votre gestionnaire de contacts
        self.contacts_manager.show()  # Affichez la fenêtre

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Erreur fatale : {str(e)}")
        sys.exit(1)