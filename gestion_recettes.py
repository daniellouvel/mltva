from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox
from PySide6.QtCore import Qt, QEvent, QDate
from ui.ui_gestion_Recettes import Ui_Dialog  # Importer l'interface générée
from util import (
    PeriodeManager,
    convert_month_to_number,
    calculate_tva,
    validate_fields,
    update_button_color,
    configure_fournisseur_combobox,
    handle_exception,
)
from database import DatabaseManager
from datetime import datetime
from calculette import CalculetteDialog  # Modification ici
from constants import UI_CONFIG  # Importer UI_CONFIG


class GestionRecettes(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Initialisation du gestionnaire de période
        self.periode_manager = PeriodeManager()
        self.mois, self.annee = self.periode_manager.get_periode()

        # Initialisation de la base de données
        self.db_manager = DatabaseManager("data/mlbdd.db")
        print("Connexion à la base de données établie.")

        # Configuration du tableau
        self.configure_table()

        # Masquer le calendrier au départ
        self.ui.calendarWidget.setVisible(False)

        # Charger les données dans la table
        self.load_periode()

        # Configurer les interactions avec le calendrier
        self.ui.lineEditDate.mousePressEvent = self.show_calendar_on_focus
        self.ui.calendarWidget.clicked.connect(self.on_calendar_date_clicked)

        # Configurer les combobox
        configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)
        self.configure_payment_combobox()  # Configuration du comboBoxpayment
        self.configure_tva_combobox()  # Configuration du comboBoxTVA

        # Connexion des boutons
        self.ui.quitterButton.clicked.connect(self.close)
        self.ui.pushButtonValider.clicked.connect(self.add_new_row)
        self.ui.pushButtonModifier.clicked.connect(self.update_row)
        self.ui.pushButtonSuprimer.clicked.connect(self.delete_row)
        self.ui.pushButtonEffacer.clicked.connect(self.clear_fields)

        # Connexion du bouton pour ouvrir la calculette
        self.ui.push_calculettettc.clicked.connect(self.open_calculette)  # Ajout de la connexion

        # Connecter les événements pour calculer le montant de la TVA
        self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
        self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)

        # Gestion de la sélection d'une ligne dans la table
        self.ui.tableWidget.cellClicked.connect(self.load_selected_row)

        # Variable pour stocker l'ID de la ligne sélectionnée
        self.selected_row_id = None

        # Configuration des boutons par défaut
        self.ui.pushButtonValider.setDefault(True)
        self.ui.quitterButton.setAutoDefault(False)
        self.ui.quitterButton.setDefault(False)

        # Désactivation de la fermeture avec la touche Entrée
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)

        # Installation d'un filtre d'événements pour tous les widgets
        self.installEventFilter(self)

        # Initialisation du champ de TVA en lecture seule
        self.ui.lineEditMontantTVA.setReadOnly(True)

        # Mettre le focus sur lineEditDate
        self.ui.lineEditDate.setFocus()  # Placer le focus sur lineEditDate

    def eventFilter(self, obj, event):
        """Filtre les événements pour gérer la touche Entrée."""
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if isinstance(obj, (QLineEdit, QComboBox)):
                    return False
                if obj == self.ui.quitterButton:
                    return False
                if obj == self.ui.tableWidget:
                    return False
                self.add_new_row()
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        """Gère les événements de clavier globaux."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if isinstance(self.focusWidget(), (QLineEdit, QComboBox)):
                return
            if self.focusWidget() == self.ui.quitterButton:
                return
            if self.focusWidget() == self.ui.tableWidget:
                return
            self.add_new_row()
        else:
            super().keyPressEvent(event)

    def configure_table(self):
        """Configure les en-têtes et les largeurs des colonnes du tableau."""
        self.ui.tableWidget.setColumnCount(9)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["Repère", "Date", "Client", "Paiement", "N° Facture", "Montant", "Taux TVA", "Montant TVA", "Commentaire"]
        )
        self.ui.tableWidget.verticalHeader().setVisible(False)  # Masquer les numéros de ligne
        self.set_column_widths()

    def set_column_widths(self):
        """Définit une largeur fixe pour chaque colonne."""
        self.ui.tableWidget.setColumnWidth(0, 50)   # Colonne 0 : Repère
        self.ui.tableWidget.setColumnWidth(1, 100)  # Colonne 1 : Date
        self.ui.tableWidget.setColumnWidth(2, 185)  # Colonne 2 : Client
        self.ui.tableWidget.setColumnWidth(3, 80)   # Colonne 3 : Paiement
        self.ui.tableWidget.setColumnWidth(4, 80)   # Colonne 4 : N° Facture
        self.ui.tableWidget.setColumnWidth(5, 100)  # Colonne 5 : Montant
        self.ui.tableWidget.setColumnWidth(6, 80)   # Colonne 6 : Taux TVA
        self.ui.tableWidget.setColumnWidth(7, 100)  # Colonne 7 : Montant TVA
        self.ui.tableWidget.setColumnWidth(8, 400)  # Colonne 8 : Commentaire

    def load_periode(self):
        """Charge et affiche la période actuelle."""
        self.ui.moisLabel.setText(self.mois)
        self.ui.anneeLabel.setText(str(self.annee))
        self.selected_month = convert_month_to_number(self.mois)
        self.selected_year = int(self.annee)
        self.load_recettes()

    def show_calendar_on_focus(self, event):
        """Affiche le calendrier lorsque le champ de date est cliqué."""
        try:
            start_date = QDate(self.selected_year, self.selected_month, 1)
            if self.selected_month == 12:
                end_date = QDate(self.selected_year, 12, 31)
            else:
                next_month = QDate(self.selected_year, self.selected_month + 1, 1)
                end_date = next_month.addDays(-1)
            
            self.ui.calendarWidget.setMinimumDate(start_date)
            self.ui.calendarWidget.setMaximumDate(end_date)
            self.ui.calendarWidget.setVisible(True)
        except Exception as e:
            handle_exception(e, "Erreur lors de l'affichage du calendrier")

    def on_calendar_date_clicked(self, date):
        """Gère le clic sur une date dans le calendrier."""
        try:
            formatted_date = f"{date.day():02d}/{date.month():02d}/{date.year()}"
            self.ui.lineEditDate.setText(formatted_date)
            self.ui.calendarWidget.setVisible(False)
        except Exception as e:
            handle_exception(e, "Erreur lors de la sélection de la date")

    def load_recettes(self):
        """Charge les recettes pour la période sélectionnée et calcule les totaux."""
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
                if column_number == 1 and isinstance(data, str):  # Formatage des dates
                    try:
                        data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except ValueError:
                        pass
                item = QTableWidgetItem(str(data or ""))
                self.ui.tableWidget.setItem(row_number, column_number, item)
                total_montant += float(row_data[5] or 0)  # Colonne Montant
                total_montant_tva += float(row_data[7] or 0)  # Colonne Montant TVA
        self.update_totals(total_montant, total_montant_tva)

    def update_totals(self, total_montant, total_montant_tva):
        """Met à jour les champs de texte avec les totaux calculés."""
        self.ui.lineEdimontanttotal.setText(f"{total_montant:.2f}")
        self.ui.lineEdittotalmontanttva.setText(f"{total_montant_tva:.2f}")

    def calculate_tva(self):
        """Calcule le montant de la TVA à partir du montant TTC et du taux de TVA."""
        montant_tva = calculate_tva(self.ui.lineEditMontant.text(), self.ui.comboBoxTVA.currentText())
        if montant_tva is not None:
            self.ui.lineEditMontantTVA.setText(f"{montant_tva:.2f}")
        else:
            self.ui.lineEditMontantTVA.setText("")

    def validate_fields(self):
        """Vérifie si tous les champs obligatoires sont remplis."""
        return validate_fields(
            [
                self.ui.lineEditDate.text(),
                self.ui.comboBoxFournisseur.currentText(),
                self.ui.comboBoxpayment.currentText(),  # Remplace lineEditpayment.text()
                self.ui.lineEditMontant.text(),
                self.ui.comboBoxTVA.currentText(),
                self.ui.lineEditMontantTVA.text(),
            ]
        )

    def configure_payment_combobox(self):
        """Configure les options disponibles pour le mode de paiement."""
        self.ui.comboBoxpayment.clear()
        self.ui.comboBoxpayment.addItems(["null", "chèque", "virement"])

    def configure_tva_combobox(self):
        """Configure les options disponibles pour le taux de TVA."""
        self.ui.comboBoxTVA.clear()  # Effacer les anciennes valeurs
        self.ui.comboBoxTVA.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])  # Ajouter les taux de TVA

    def add_new_row(self):
        """Ajoute une nouvelle recette dans la table 'recettes'."""
        if not self.validate_fields():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
            return
        try:
            date_text = self.ui.lineEditDate.text()
            client = self.ui.comboBoxFournisseur.currentText()
            paiement = self.ui.comboBoxpayment.currentText()
            numero_facture = self.ui.lineEditnfacture.text()
            montant_text = self.ui.lineEditMontant.text()
            tva_rate_text = self.ui.comboBoxTVA.currentText()
            montant_tva_text = self.ui.lineEditMontantTVA.text()
            commentaire = self.ui.lineEditComentaire.text()
            date_obj = datetime.strptime(date_text, "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            montant = float(montant_text)
            tva_rate = float(tva_rate_text.strip('%'))
            montant_tva = float(montant_tva_text)

            # Vérifier si le client existe
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
                self.load_recettes()
                self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de l'ajout de la recette")

    def clear_fields(self):
        """Efface tous les champs de saisie pour préparer une nouvelle entrée."""
        self.ui.lineEditDate.clear()
        self.ui.comboBoxFournisseur.setCurrentIndex(-1)
        self.ui.comboBoxpayment.setCurrentIndex(-1)  # Réinitialise comboBoxpayment
        self.ui.lineEditnfacture.clear()
        self.ui.lineEditMontant.clear()
        self.ui.comboBoxTVA.setCurrentIndex(0)  # Réinitialise comboBoxTVA
        self.ui.lineEditMontantTVA.clear()
        self.ui.lineEditComentaire.clear()
        self.selected_row_id = None
        self.ui.pushButtonValider.setEnabled(True)

    def load_selected_row(self, row):
        """Charge les valeurs d'une ligne sélectionnée dans les champs de saisie."""
        try:
            self.selected_row_id = self.ui.tableWidget.item(row, 0).text()
            date = self.ui.tableWidget.item(row, 1).text()
            client = self.ui.tableWidget.item(row, 2).text()
            paiement = self.ui.tableWidget.item(row, 3).text()  # Valeur du mode de paiement
            numero_facture = self.ui.tableWidget.item(row, 4).text()
            montant = self.ui.tableWidget.item(row, 5).text()
            tva_rate = self.ui.tableWidget.item(row, 6).text()
            montant_tva = self.ui.tableWidget.item(row, 7).text()
            commentaire = self.ui.tableWidget.item(row, 8).text()

            if paiement in ["null", "chèque", "virement"]:
                self.ui.comboBoxpayment.setCurrentText(paiement)
            else:
                self.ui.comboBoxpayment.setCurrentIndex(-1)  # Réinitialiser comboBoxpayment si la valeur est invalide

            self.ui.lineEditDate.setText(date)
            self.ui.comboBoxFournisseur.setCurrentText(client)
            self.ui.lineEditnfacture.setText(numero_facture)
            self.ui.lineEditMontant.setText(montant)
            self.ui.comboBoxTVA.setCurrentText(f"{tva_rate}%")  # Charger le taux de TVA
            self.ui.lineEditMontantTVA.setText(montant_tva)
            self.ui.lineEditComentaire.setText(commentaire)

            self.ui.pushButtonValider.setEnabled(False)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la ligne sélectionnée")

    def update_row(self):
        """Modifie une recette existante dans la base de données."""
        if not self.selected_row_id:
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée.")
            return
        try:
            date_text = self.ui.lineEditDate.text()
            client = self.ui.comboBoxFournisseur.currentText()
            paiement = self.ui.comboBoxpayment.currentText()  # Remplace lineEditpayment.text()
            numero_facture = self.ui.lineEditnfacture.text()
            montant_text = self.ui.lineEditMontant.text()
            tva_rate_text = self.ui.comboBoxTVA.currentText()
            montant_tva_text = self.ui.lineEditMontantTVA.text()
            commentaire = self.ui.lineEditComentaire.text()
            date_obj = datetime.strptime(date_text, "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            montant = float(montant_text)
            tva_rate = float(tva_rate_text.strip('%'))
            montant_tva = float(montant_tva_text)
            success = self.db_manager.update_recette(
                self.selected_row_id, formatted_date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire
            )
            if success:
                self.load_recettes()
                self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de la modification de la recette")

    def delete_row(self):
        """Supprime une recette existante de la base de données."""
        if not self.selected_row_id:
            QMessageBox.warning(self, "Erreur", "Aucune ligne sélectionnée.")
            return
        try:
            row = self.ui.tableWidget.currentRow()
            date = self.ui.tableWidget.item(row, 1).text()
            client = self.ui.tableWidget.item(row, 2).text()
            paiement = self.ui.tableWidget.item(row, 3).text()
            numero_facture = self.ui.tableWidget.item(row, 4).text()
            montant = self.ui.tableWidget.item(row, 5).text()
            tva_rate = self.ui.tableWidget.item(row, 6).text()
            montant_tva = self.ui.tableWidget.item(row, 7).text()
            commentaire = self.ui.tableWidget.item(row, 8).text()

            confirmation_message = (
                f"Êtes-vous sûr de vouloir supprimer cette recette ?\n\n"
                f"Date : {date}\n"
                f"Client : {client}\n"
                f"Paiement : {paiement}\n"
                f"N° Facture : {numero_facture}\n"
                f"Montant : {montant}\n"
                f"Taux TVA : {tva_rate}\n"
                f"Montant TVA : {montant_tva}\n"
                f"Commentaire : {commentaire}"
            )
            reply = QMessageBox.question(
                self,
                "Confirmation de suppression",
                confirmation_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_recette(self.selected_row_id)
                if success:
                    self.load_recettes()
                    self.clear_fields()
        except Exception as e:
            handle_exception(e, "Erreur lors de la suppression de la recette")

    def open_calculette(self):
        """Ouvre la calculette."""
        self.calculette_window = CalculetteDialog(self)  # Passer l'instance de GestionRecettes
        montant_value = self.ui.lineEditMontant.text()  # Récupérer la valeur du montant
        tva_value = self.ui.comboBoxTVA.currentText()  # Récupérer la valeur du taux de TVA
        self.calculette_window.set_initial_values(tva_value, montant_value)  # Définir la valeur dans la calculette
        self.calculette_window.exec()  # Affichez la fenêtre de la calculette