from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox
from PySide6.QtCore import Qt, QEvent, QDate
from ui.ui_gestion_Recettes import Ui_Dialog
from ui.base_gestion import GestionBase
from util import (
    PeriodeManager,
    convert_month_to_number,
    calculate_tva,
    validate_fields,
    configure_fournisseur_combobox,
    handle_exception,
)
from database import DatabaseManager
from datetime import datetime
from constants import UI_CONFIG


class GestionRecettes(GestionBase):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.periode_manager = PeriodeManager()
        self.mois, self.annee = self.periode_manager.get_periode()
        self.db_manager = DatabaseManager()
        self.selected_row_id = None

        self.configure_table()
        self.ui.calendarWidget.setVisible(False)
        self.load_periode()

        self.ui.lineEditDate.mousePressEvent = self.show_calendar_on_focus
        self.ui.calendarWidget.clicked.connect(self.on_calendar_date_clicked)

        configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)
        self.configure_payment_combobox()
        self.configure_tva_combobox()

        self.ui.quitterButton.clicked.connect(self.close)
        self.ui.pushButtonValider.clicked.connect(self.add_new_row)
        self.ui.pushButtonModifier.clicked.connect(self.update_row)
        self.ui.pushButtonSupprimer.clicked.connect(self.delete_row)
        self.ui.pushButtonEffacer.clicked.connect(self.clear_fields)
        self.ui.push_calculettettc.clicked.connect(self.calculate_and_update)
        self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
        self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)
        self.ui.tableWidget.cellClicked.connect(self.load_selected_row)

        self.ui.pushButtonValider.setDefault(True)
        self.ui.quitterButton.setAutoDefault(False)
        self.ui.quitterButton.setDefault(False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.installEventFilter(self)
        self.ui.lineEditMontantTVA.setReadOnly(True)
        self.ui.lineEditDate.setFocus()

    def configure_table(self):
        self.ui.tableWidget.setColumnCount(9)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Repère", "Date", "Client", "Paiement", "N° Facture", "Montant", "Taux TVA", "Montant TVA", "Commentaire"]
        )
        self.ui.tableWidget.verticalHeader().setVisible(False)
        widths = [50, 100, 185, 80, 80, 100, 80, 100, 400]
        for col, width in enumerate(widths):
            self.ui.tableWidget.setColumnWidth(col, width)

    def load_periode(self):
        self.ui.moisLabel.setText(self.mois)
        self.ui.anneeLabel.setText(str(self.annee))
        self.selected_month = convert_month_to_number(self.mois)
        self.selected_year = int(self.annee)
        self.load_recettes()

    def load_recettes(self):
        mois_numerique = convert_month_to_number(self.mois)
        query = """
        SELECT id, date, client, paiement, numero_facture, montant, tva, montant_tva, commentaire
        FROM recettes
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
        """
        rows = self.db_manager.fetch_all(query, (f"{mois_numerique:02d}", self.annee))
        self.ui.tableWidget.setRowCount(0)
        total_montant = 0.0
        total_montant_tva = 0.0
        for row_number, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 1 and isinstance(data, str):
                    try:
                        data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except ValueError:
                        pass
                self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data or "")))
            total_montant += float(row_data[5] or 0)
            total_montant_tva += float(row_data[7] or 0)
        self.ui.lineEditMontantTotal.setText(f"{total_montant:.2f}")
        self.ui.lineEditTotalMontantTVA.setText(f"{total_montant_tva:.2f}")

    def validate_fields(self):
        return validate_fields(
            self.ui.lineEditDate.text(),
            self.ui.comboBoxFournisseur.currentText(),
            self.ui.comboBoxPaiement.currentText(),
            self.ui.lineEditMontant.text(),
            self.ui.comboBoxTVA.currentText(),
            self.ui.lineEditMontantTVA.text(),
        )

    def configure_payment_combobox(self):
        self.ui.comboBoxPaiement.clear()
        self.ui.comboBoxPaiement.addItems(["null", "chèque", "virement"])

    def configure_tva_combobox(self):
        self.ui.comboBoxTVA.clear()
        self.ui.comboBoxTVA.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])

    def add_new_row(self):
        if not self.validate_fields():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return
        try:
            date_obj = datetime.strptime(self.ui.lineEditDate.text(), "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            client = self.ui.comboBoxFournisseur.currentText()
            paiement = self.ui.comboBoxPaiement.currentText()
            numero_facture = self.ui.lineEditnfacture.text()
            montant = float(self.ui.lineEditMontant.text())
            tva_rate = float(self.ui.comboBoxTVA.currentText().strip('%'))
            montant_tva = float(self.ui.lineEditMontantTVA.text())
            commentaire = self.ui.lineEditCommentaire.text()
            if not self.db_manager.client_exists(client):
                response = QMessageBox.question(self, "Client non trouvé",
                                                f"Le client '{client}' n'existe pas. Voulez-vous l'ajouter ?",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    self.db_manager.insert_client(client)
                    configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)
            success = self.db_manager.insert_recette(
                formatted_date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire
            )
            if success:
                QMessageBox.information(self, "Succès", "La recette a été ajoutée avec succès.")
                self.load_recettes()
                self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de l'ajout de la recette")

    def clear_fields(self):
        self.ui.lineEditDate.clear()
        self.ui.comboBoxFournisseur.setCurrentIndex(-1)
        self.ui.comboBoxPaiement.setCurrentIndex(-1)
        self.ui.lineEditnfacture.clear()
        self.ui.lineEditMontant.clear()
        self.ui.comboBoxTVA.setCurrentIndex(0)
        self.ui.lineEditMontantTVA.clear()
        self.ui.lineEditCommentaire.clear()
        self.selected_row_id = None
        self.ui.pushButtonValider.setEnabled(True)

    def load_selected_row(self, row):
        try:
            self.selected_row_id = self.ui.tableWidget.item(row, 0).text()
            paiement = self.ui.tableWidget.item(row, 3).text()
            self.ui.lineEditDate.setText(self.ui.tableWidget.item(row, 1).text())
            self.ui.comboBoxFournisseur.setCurrentText(self.ui.tableWidget.item(row, 2).text())
            if paiement in ["null", "chèque", "virement"]:
                self.ui.comboBoxPaiement.setCurrentText(paiement)
            else:
                self.ui.comboBoxPaiement.setCurrentIndex(-1)
            self.ui.lineEditnfacture.setText(self.ui.tableWidget.item(row, 4).text())
            self.ui.lineEditMontant.setText(self.ui.tableWidget.item(row, 5).text())
            self.ui.comboBoxTVA.setCurrentText(f"{self.ui.tableWidget.item(row, 6).text()}%")
            self.ui.lineEditMontantTVA.setText(self.ui.tableWidget.item(row, 7).text())
            self.ui.lineEditCommentaire.setText(self.ui.tableWidget.item(row, 8).text())
            self.ui.pushButtonValider.setEnabled(False)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la ligne sélectionnée")

    def update_row(self):
        if not self.selected_row_id:
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée.")
            return
        try:
            date_obj = datetime.strptime(self.ui.lineEditDate.text(), "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            client = self.ui.comboBoxFournisseur.currentText()
            paiement = self.ui.comboBoxPaiement.currentText()
            numero_facture = self.ui.lineEditnfacture.text()
            montant = float(self.ui.lineEditMontant.text())
            tva_rate = float(self.ui.comboBoxTVA.currentText().strip('%'))
            montant_tva = float(self.ui.lineEditMontantTVA.text())
            commentaire = self.ui.lineEditCommentaire.text()
            success = self.db_manager.update_recette(
                self.selected_row_id, formatted_date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire
            )
            if success:
                self.load_recettes()
                self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de la modification de la recette")

    def delete_row(self):
        if not self.selected_row_id:
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée.")
            return
        try:
            row = self.ui.tableWidget.currentRow()
            confirmation_message = (
                f"Êtes-vous sûr de vouloir supprimer cette recette ?\n\n"
                f"Date : {self.ui.tableWidget.item(row, 1).text()}\n"
                f"Client : {self.ui.tableWidget.item(row, 2).text()}\n"
                f"Montant : {self.ui.tableWidget.item(row, 5).text()}"
            )
            reply = QMessageBox.question(self, "Confirmation de suppression", confirmation_message,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_recette(self.selected_row_id)
                if success:
                    self.load_recettes()
                    self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de la suppression de la recette")

