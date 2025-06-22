# gestion_forniseur_a_regler.py

from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QVBoxLayout, QHBoxLayout, QFileDialog
from ui.ui_gestion_forniseur_a_regler import Ui_Dialog
from database import DatabaseManager
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pdf_generator import PDFGenerator  # Importer la classe PDFGenerator

class GestionFournisseurARegler(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Initialisation de la base de données
        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator(self.db_manager)  # Créer une instance de PDFGenerator

        # Charger les données dans le tableau
        self.load_depenses()

        # Connexion des boutons
        self.ui.pushButtonValider.clicked.connect(self.on_valider_clicked)
        self.ui.pushButton_export_pdf.clicked.connect(self.export_pdf)  # Connexion du bouton PDF
        self.ui.quitterButton.clicked.connect(self.close)

        # Améliorer l'apparence de l'interface
        self.setup_ui()

        # Ajuster la taille de la fenêtre après la configuration
        self.adjustSize()  # Ajuste la taille de la fenêtre à son contenu

    def setup_ui(self):
        """Configure l'apparence de l'interface."""
        # Ajuster les largeurs des colonnes
        self.ui.tableWidget_a_regler.setColumnWidth(0, 50)  # Colonne ID
        self.ui.tableWidget_a_regler.setColumnWidth(1, 100)  # Colonne Date
        self.ui.tableWidget_a_regler.setColumnWidth(2, 185)  # Colonne Fournisseur
        self.ui.tableWidget_a_regler.setColumnWidth(3, 80)   # Colonne TTC

    def load_depenses(self):
        """Charge les dépenses dans le tableau où la validation n'est pas 'Oui'."""
        try:
            # Exclure la colonne 'validation' de la requête
            query = "SELECT id, date, fournisseur, ttc FROM depenses WHERE validation != 'Oui'"
            rows = self.db_manager.fetch_all(query)

            self.ui.tableWidget_a_regler.setRowCount(0)  # Réinitialiser le tableau
            total_ttc = 0.0  # Initialiser la somme des montants ttc

            for row_number, row_data in enumerate(rows):
                self.ui.tableWidget_a_regler.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == 1:  # Colonne date
                        # Formatage de la date au format dd/mm/yyyy
                        date_obj = datetime.strptime(data, "%Y-%m-%d")  # Assurez-vous que le format d'origine est correct
                        formatted_date = date_obj.strftime("%d/%m/%Y")
                        item = QTableWidgetItem(formatted_date)
                    elif column_number == 2:  # Colonne fournisseur
                        item = QTableWidgetItem(str(data))
                    elif column_number == 3:  # Colonne ttc
                        # Formatage de la valeur ttc
                        formatted_ttc = f"{data:,.2f} €".replace(',', ' ').replace('.', ',')
                        item = QTableWidgetItem(formatted_ttc)
                    else:
                        item = QTableWidgetItem(str(data))
                    self.ui.tableWidget_a_regler.setItem(row_number, column_number, item)

                # Ajouter à la somme des montants ttc
                total_ttc += float(row_data['ttc']) if row_data['ttc'] is not None else 0.0

            # Mettre à jour le champ lineEdittotalttc avec la somme formatée
            self.ui.lineEdittotalttc.setText(f"{total_ttc:,.2f} €".replace(',', ' ').replace('.', ','))

            # Redimensionner la colonne 'fournisseur' pour s'adapter au contenu
            self.ui.tableWidget_a_regler.resizeColumnToContents(2)  # Index de la colonne 'fournisseur'

            # Cacher la colonne 'validation' (index 4)
            self.ui.tableWidget_a_regler.setColumnHidden(4, True)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des dépenses : {str(e)}")

    def on_valider_clicked(self):
        """Méthode appelée lorsque le bouton 'Valider' est cliqué."""
        selected_rows = self.ui.tableWidget_a_regler.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, "Avertissement", "Aucune ligne sélectionnée.")
            return

        # Collecte des indices de lignes uniques
        row_indices = set(item.row() for item in selected_rows)

        try:
            for row_index in row_indices:
                # Récupérer l'ID de la ligne sélectionnée
                item_id = self.ui.tableWidget_a_regler.item(row_index, 0).text()  # Supposons que l'ID est dans la première colonne
                # Mettre à jour l'état de validation dans la base de données
                self.db_manager.update_validation_status(item_id, 'Oui')  # Assurez-vous que cette méthode est bien implémentée

            self.load_depenses()  # Recharge les données pour refléter les changements
            # QMessageBox.information(self, "Information", "Validation effectuée pour les lignes sélectionnées.")  # Ligne supprimée
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la validation : {str(e)}")

    def export_pdf(self):
        """Génère un rapport PDF des dépenses."""
        query = "SELECT id, date, fournisseur, ttc FROM depenses WHERE validation != 'Oui'"
        rows = self.db_manager.fetch_all(query)

        # Définir un nom de fichier par défaut
        default_filename = "fournisseur_a_regler.pdf"

        # Ouvrir un dialogue pour choisir l'emplacement et le nom du fichier PDF
        options = QFileDialog.Options()
        pdf_file, _ = QFileDialog.getSaveFileName(self, "Enregistrer le PDF", default_filename, "PDF Files (*.pdf);;All Files (*)", options=options)

        if not pdf_file:  # Vérifier si l'utilisateur a annulé le dialogue
            return

        # Préparer les données pour le PDF
        data = [['ID', 'Date', 'Fournisseur', 'TTC']]
        total_ttc = 0.0  # Initialiser le total TTC

        for row in rows:
            # Formatage de la date au format dd/mm/yyyy
            date_obj = datetime.strptime(row[1], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")

            data.append([
                str(row[0]),  # ID
                formatted_date,  # Date formatée
                row[2],       # Fournisseur
                f"{row[3]:,.2f} €"  # TTC
            ])
            total_ttc += float(row[3])  # Ajouter au total TTC

        # Ajouter le total à la fin des données
        data.append(['', '', 'Total TTC :', f"{total_ttc:,.2f} €"])

        # Générer le PDF en utilisant PDFGenerator
        self.pdf_generator.generate_pdf(data, pdf_file)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GestionFournisseurARegler()
    window.show()
    sys.exit(app.exec())