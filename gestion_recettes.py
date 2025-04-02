from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox
from PySide6.QtCore import Qt, QEvent, QDate
from ui.ui_gestion_Recettes import Ui_Dialog  # Importer l'interface générée
from util import (
    PeriodeManager,
    convert_month_to_number,
    calculate_tva,
    validate_fields,
    update_button_color,
    configure_fournisseur_combobox,  # Remplacement de configure_client_combobox
    handle_exception,
)
from database import DatabaseManager
from datetime import datetime, timedelta


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
        configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)  # Utilisation de configure_fournisseur_combobox
        self.configure_payment_combobox()  # Configuration du comboBoxpayment
        self.configure_tva_combobox()  # Configuration du comboBoxTVA

        # Connexion des boutons
        self.ui.quitterButton.clicked.connect(self.close)
        self.ui.pushButtonValider.clicked.connect(self.add_new_row)
        self.ui.pushButtonModifier.clicked.connect(self.update_row)
        self.ui.pushButtonSuprimer.clicked.connect(self.delete_row)
        self.ui.pushButtonEffacer.clicked.connect(self.clear_fields)

        # Connecter les événements pour calculer le montant de la TVA
        self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
        self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)
        self.ui.lineEditMontant_2.textChanged.connect(self.calculate_tva_2)
        self.ui.comboBoxTVA_2.currentTextChanged.connect(self.calculate_tva_2)

        # Gestion de la sélection d'une ligne dans la table
        self.ui.tableWidget.cellClicked.connect(self.load_selected_row)

        # Variable pour stocker l'ID de la ligne sélectionnée
        self.selected_row_id = None

        # Gestion de la visibilité de Saisie2em2ligne
        self.ui.checkBox2emeLigne.stateChanged.connect(self.toggle_saisie_2eme_ligne)
        self.ui.Saisie2em2ligne.setVisible(False)

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

    def eventFilter(self, obj, event):
        """Filtre les événements pour gérer la touche Entrée."""
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                # Si le focus est sur un champ de saisie ou une combobox, ne rien faire
                if isinstance(obj, (QLineEdit, QComboBox)):
                    return False
                # Si le focus est sur le bouton Quitter, ne rien faire
                if obj == self.ui.quitterButton:
                    return False
                # Si le focus est sur le tableau, ne rien faire
                if obj == self.ui.tableWidget:
                    return False
                # Sinon, simuler un clic sur le bouton Valider
                self.add_new_row()
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        """Gère les événements de clavier globaux."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Si le focus est sur un champ de saisie ou une combobox, ne rien faire
            if isinstance(self.focusWidget(), (QLineEdit, QComboBox)):
                return
            # Si le focus est sur le bouton Quitter, ne rien faire
            if self.focusWidget() == self.ui.quitterButton:
                return
            # Si le focus est sur le tableau, ne rien faire
            if self.focusWidget() == self.ui.tableWidget:
                return
            # Sinon, simuler un clic sur le bouton Valider
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

    def toggle_saisie_2eme_ligne(self):
        """Affiche ou masque le cadre Saisie2em2ligne en fonction de l'état de checkBox2emeLigne."""
        is_checked = self.ui.checkBox2emeLigne.isChecked()
        self.ui.Saisie2em2ligne.setVisible(is_checked)

        # Désactiver/activer le calcul automatique de la TVA
        if is_checked:
            # Désactiver les connexions pour le calcul de TVA
            self.ui.lineEditMontant.textChanged.disconnect(self.calculate_tva)
            self.ui.comboBoxTVA.currentTextChanged.disconnect(self.calculate_tva)
            self.ui.lineEditMontant_2.textChanged.disconnect(self.calculate_tva_2)
            self.ui.comboBoxTVA_2.currentTextChanged.disconnect(self.calculate_tva_2)
            # Initialiser le montant de la deuxième ligne à 0
            self.ui.lineEditMontant_2.setText("0")
            # Rendre le champ de TVA modifiable
            self.ui.lineEditMontantTVA.setReadOnly(False)
        else:
            # Réactiver les connexions pour le calcul de TVA
            self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
            self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)
            self.ui.lineEditMontant_2.textChanged.connect(self.calculate_tva_2)
            self.ui.comboBoxTVA_2.currentTextChanged.connect(self.calculate_tva_2)
            # Rendre le champ de TVA non modifiable
            self.ui.lineEditMontantTVA.setReadOnly(True)

        # Configuration des boutons par défaut
        self.ui.pushButtonValider.setDefault(True)
        self.ui.quitterButton.setAutoDefault(False)
        self.ui.quitterButton.setDefault(False)

        # Désactivation de la fermeture avec la touche Entrée
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)

    def load_periode(self):
        """Charge et affiche la période actuelle."""
        self.ui.moisLabel.setText(self.mois)
        self.ui.anneeLabel.setText(str(self.annee))
        self.selected_month = convert_month_to_number(self.mois)
        self.selected_year = int(self.annee)
        # On ne configure plus le calendrier ici
        self.load_recettes()

    def configure_calendar(self):
        """Configure le calendrier pour restreindre les dates à la période sélectionnée."""
        start_date = datetime(self.selected_year, self.selected_month, 1)
        end_date = (
            datetime(self.selected_year + 1, 1, 1)
            if self.selected_month == 12
            else datetime(self.selected_year, self.selected_month + 1, 1)
        )
        self.ui.calendarWidget.setMinimumDate(start_date)
        self.ui.calendarWidget.setMaximumDate(end_date)

    def show_calendar_on_focus(self, event):
        """Affiche le calendrier lorsque le champ de date est cliqué."""
        try:
            # Configuration des dates minimum et maximum pour la période sélectionnée
            start_date = QDate(self.selected_year, self.selected_month, 1)
            
            # Calcul de la date de fin (dernier jour du mois)
            if self.selected_month == 12:
                end_date = QDate(self.selected_year, 12, 31)
            else:
                # On prend le premier jour du mois suivant et on soustrait 1 jour
                next_month = QDate(self.selected_year, self.selected_month + 1, 1)
                end_date = next_month.addDays(-1)
            
            # Configuration des dates
            self.ui.calendarWidget.setMinimumDate(start_date)
            self.ui.calendarWidget.setMaximumDate(end_date)
            
            # Affichage du calendrier
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

    def calculate_tva_2(self):
        """Calcule le montant de la TVA pour la deuxième ligne."""
        montant_tva = calculate_tva(self.ui.lineEditMontant_2.text(), self.ui.comboBoxTVA_2.currentText())
        if montant_tva is not None:
            self.ui.lineEditMontantTVA_2.setText(f"{montant_tva:.2f}")
        else:
            self.ui.lineEditMontantTVA_2.setText("")

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
        self.ui.comboBoxTVA.clear()
        self.ui.comboBoxTVA.addItems(["0%", "5.5%", "10%", "20%"])

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
                # Demander à l'utilisateur s'il souhaite ajouter le client
                response = QMessageBox.question(self, "Client non trouvé",
                                                f"Le client '{client}' n'existe pas. Voulez-vous l'ajouter ?",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    # Ajouter le client à la base de données
                    self.db_manager.insert_client(client)
                    # Mettre à jour la combobox des clients
                    configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)

            # Insérer la recette dans la base de données
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
        self.ui.lineEditMontant_2.clear()
        self.ui.comboBoxTVA_2.setCurrentIndex(0)
        self.ui.lineEditMontantTVA_2.clear()
        self.ui.lineEditComentaire_2.clear()
        self.ui.checkBox2emeLigne.setChecked(False)
        self.selected_row_id = None
        # Réactiver les éléments
        self.ui.pushButtonValider.setEnabled(True)
        self.ui.checkBox2emeLigne.setEnabled(True)

    def load_selected_row(self, row):
        """Charge les valeurs d'une ligne sélectionnée dans les champs de saisie."""
        try:
            # Réinitialiser les champs avant de charger une nouvelle ligne
            self.clear_fields()

            # Récupérer les données de la ligne sélectionnée
            self.selected_row_id = self.ui.tableWidget.item(row, 0).text()
            date = self.ui.tableWidget.item(row, 1).text()
            client = self.ui.tableWidget.item(row, 2).text()
            paiement = self.ui.tableWidget.item(row, 3).text()  # Valeur du mode de paiement
            numero_facture = self.ui.tableWidget.item(row, 4).text()
            montant = self.ui.tableWidget.item(row, 5).text()
            tva_rate = self.ui.tableWidget.item(row, 6).text()
            montant_tva = self.ui.tableWidget.item(row, 7).text()
            commentaire = self.ui.tableWidget.item(row, 8).text()

            # Vérifier si la valeur de paiement existe dans les options du comboBoxpayment
            if paiement in ["null", "chèque", "virement"]:
                self.ui.comboBoxpayment.setCurrentText(paiement)
            else:
                self.ui.comboBoxpayment.setCurrentIndex(-1)  # Réinitialiser comboBoxpayment si la valeur est invalide

            # Charger les autres champs
            self.ui.lineEditDate.setText(date)
            self.ui.comboBoxFournisseur.setCurrentText(client)
            self.ui.lineEditnfacture.setText(numero_facture)
            self.ui.lineEditMontant.setText(montant)
            self.ui.comboBoxTVA.setCurrentText(f"{tva_rate}%")  # Charger le taux de TVA
            self.ui.lineEditMontantTVA.setText(montant_tva)
            self.ui.lineEditComentaire.setText(commentaire)

            # Désactiver les boutons Valider et checkBox2emeLigne
            self.ui.pushButtonValider.setEnabled(False)
            self.ui.checkBox2emeLigne.setEnabled(False)

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
            # Récupérer les informations de la ligne à supprimer
            row = self.ui.tableWidget.currentRow()
            date = self.ui.tableWidget.item(row, 1).text()
            client = self.ui.tableWidget.item(row, 2).text()
            paiement = self.ui.tableWidget.item(row, 3).text()
            numero_facture = self.ui.tableWidget.item(row, 4).text()
            montant = self.ui.tableWidget.item(row, 5).text()
            tva_rate = self.ui.tableWidget.item(row, 6).text()
            montant_tva = self.ui.tableWidget.item(row, 7).text()
            commentaire = self.ui.tableWidget.item(row, 8).text()

            # Demander confirmation avec un rappel des valeurs
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