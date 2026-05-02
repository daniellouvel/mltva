from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QVBoxLayout, QTableWidget, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QEvent, QDate
from ui.ui_gestion_depenses import Ui_Dialog
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
from constants import ERROR_MESSAGES, UI_CONFIG
from calculette import CalculetteDialog  # Modification ici

# Configuration des colonnes du tableau
TABLE_COLUMNS = {
    "REPERE": 0,
    "DATE": 1,
    "FOURNISSEUR": 2,
    "TTC": 3,
    "TVA_RATE": 4,
    "TVA_AMOUNT": 5,
    "VALIDATION": 6,
    "COMMENTAIRE": 7
}

# Largeurs des colonnes
COLUMN_WIDTHS = {
    TABLE_COLUMNS["REPERE"]: 50,
    TABLE_COLUMNS["DATE"]: 100,
    TABLE_COLUMNS["FOURNISSEUR"]: 185,
    TABLE_COLUMNS["TTC"]: 80,
    TABLE_COLUMNS["TVA_RATE"]: 80,
    TABLE_COLUMNS["TVA_AMOUNT"]: 100,
    TABLE_COLUMNS["VALIDATION"]: 80,
    TABLE_COLUMNS["COMMENTAIRE"]: 400
}

# En-têtes des colonnes
COLUMN_HEADERS = [
    "Repère", "Date", "Fournisseur", "TTC", "Taux TVA", "Montant TVA", "Validation", "Commentaire"
]

class GestionDepenses(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Initialisation des attributs
        self.selected_row_id = None
        self.periode_manager = PeriodeManager()
        self.mois, self.annee = self.periode_manager.get_periode()
        self.db_manager = DatabaseManager("data/mlbdd.db")

        # Configuration de l'interface
        self._setup_ui()
        
        # Chargement des données
        self.load_periode()
        self.load_depenses()

        # Mettre le focus sur lineEditDate
        self.ui.lineEditDate.setFocus()  # Placer le focus sur lineEditDate

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Configuration du tableau
        self.configure_table()

        # Configuration du calendrier
        self.ui.calendarWidget.setVisible(UI_CONFIG["CALENDAR_VISIBLE"])
        self.ui.lineEditDate.mousePressEvent = self.show_calendar_on_focus
        self.ui.calendarWidget.clicked.connect(self.on_calendar_date_clicked)
        
        # Réinitialisation du champ de date
        self.ui.lineEditDate.clear()

        # Configuration des combobox
        configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)
        self.ui.comboBoxTVA.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])

        # Connexion des boutons
        self._connect_buttons()

        # Connexion des événements
        self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
        self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)
        self.ui.tableWidget.cellClicked.connect(self.load_selected_row)

        # Connexion du bouton pour calculer directement
        self.ui.push_calculettettc.clicked.connect(self.calculate_and_update)  # Connexion du bouton

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

    def _connect_buttons(self):
        """Connecte tous les boutons de l'interface."""
        button_connections = {
            "quitterButton": self.close,
            "pushButtonValider": self.add_new_row,
            "pushButtonModifier": self.update_row,
            "pushButtonSuprimer": self.delete_row,
            "pushButtonEffacer": self.clear_fields
        }

        for button_name, callback in button_connections.items():
            if hasattr(self.ui, button_name):
                getattr(self.ui, button_name).clicked.connect(callback)
            else:
                print(f"Erreur : Le bouton '{button_name}' n'existe pas dans le fichier .ui.")

    def configure_table(self):
        """Configure les en-têtes et les largeurs des colonnes du tableau."""
        try:
            self.ui.tableWidget.setColumnCount(len(COLUMN_HEADERS))
            self.ui.tableWidget.setHorizontalHeaderLabels(COLUMN_HEADERS)
            self.ui.tableWidget.verticalHeader().setVisible(False)
            self.set_column_widths()
        except Exception as e:
            handle_exception(e, "Erreur lors de la configuration du tableau")

    def set_column_widths(self):
        """Définit une largeur fixe pour chaque colonne."""
        try:
            for col, width in COLUMN_WIDTHS.items():
                self.ui.tableWidget.setColumnWidth(col, width)
        except Exception as e:
            handle_exception(e, "Erreur lors de la définition des largeurs de colonnes")

    def load_periode(self):
        """Charge et affiche la période actuelle."""
        try:
            self.ui.moisLabel.setText(self.mois)
            self.ui.anneeLabel.setText(str(self.annee))
            self.selected_month = convert_month_to_number(self.mois)
            self.selected_year = int(self.annee)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la période")

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

    def load_depenses(self):
        """Charge les dépenses pour la période sélectionnée et calcule les totaux."""
        try:
            mois_numerique = convert_month_to_number(self.mois)
            query = """
            SELECT id, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire
            FROM depenses
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            """
            rows = self.db_manager.fetch_all(query, (f"{mois_numerique:02d}", self.annee))
            
            self.ui.tableWidget.setRowCount(0)
            total_ttc = 0.0
            total_montant_tva = 0.0

            for row_number, row_data in enumerate(rows):
                self.ui.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == TABLE_COLUMNS["DATE"] and isinstance(data, str):
                        try:
                            date_obj = datetime.strptime(data, "%Y-%m-%d")
                            data = date_obj.strftime("%d/%m/%Y")
                        except ValueError:
                            pass
                    
                    item = QTableWidgetItem(str(data or ""))
                    
                    if column_number == TABLE_COLUMNS["VALIDATION"]:
                        if data == "Non":
                            item.setForeground(Qt.red)
                        elif data == "Oui":
                            item.setForeground(Qt.green)
                    
                    self.ui.tableWidget.setItem(row_number, column_number, item)
                    
                    if column_number == TABLE_COLUMNS["TTC"]:
                        total_ttc += float(data or 0)
                    elif column_number == TABLE_COLUMNS["TVA_AMOUNT"]:
                        total_montant_tva += float(data or 0)

            self.update_totals(total_ttc, total_montant_tva)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement des dépenses")

    def update_totals(self, total_ttc, total_montant_tva):
        """Met à jour les champs de texte avec les totaux calculés."""
        try:
            self.ui.lineEdittotalttc.setText(f"{total_ttc:.2f}")
            self.ui.lineEditmontanttva.setText(f"{total_montant_tva:.2f}")
        except Exception as e:
            handle_exception(e, "Erreur lors de la mise à jour des totaux")

    def calculate_tva(self):
        """Calcule le montant de la TVA à partir du montant TTC et du taux de TVA."""
        try:
            montant_tva = calculate_tva(self.ui.lineEditMontant.text(), self.ui.comboBoxTVA.currentText())
            if montant_tva is not None:
                self.ui.lineEditMontantTVA.setText(f"{montant_tva:.2f}")
            else:
                self.ui.lineEditMontantTVA.setText("")
        except Exception as e:
            handle_exception(e, "Erreur lors du calcul de la TVA")

    def validate_fields(self):
        """Vérifie si tous les champs obligatoires sont remplis."""
        try:
            required_fields = [
                self.ui.lineEditDate.text(),
                self.ui.comboBoxFournisseur.currentText(),
                self.ui.lineEditMontant.text(),
                self.ui.comboBoxTVA.currentText(),
                self.ui.lineEditMontantTVA.text(),
            ]
            
            if not validate_fields(*required_fields):
                QMessageBox.warning(self, "Attention", ERROR_MESSAGES["MISSING_FIELDS"])
                return False
                
            return True
        except Exception as e:
            handle_exception(e, "Erreur lors de la validation des champs")
            return False

    def _get_depense_data(self):
        """Récupère et valide les données de dépense depuis l'interface."""
        try:
            date_text = self.ui.lineEditDate.text()
            fournisseur = self.ui.comboBoxFournisseur.currentText()
            ttc_text = self.ui.lineEditMontant.text()
            tva_rate_text = self.ui.comboBoxTVA.currentText()
            montant_tva_text = self.ui.lineEditMontantTVA.text()
            commentaire = self.ui.lineEditComentaire.text()
            validation = "Oui" if self.ui.checkBoxValidation.isChecked() else "Non"

            if not ttc_text.replace('.', '', 1).isdigit():
                raise ValueError(ERROR_MESSAGES["INVALID_AMOUNT"])
            if not tva_rate_text.endswith('%'):
                raise ValueError(ERROR_MESSAGES["INVALID_TVA"])

            date_obj = datetime.strptime(date_text, "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            ttc = float(ttc_text)
            tva_rate = float(tva_rate_text.strip('%'))
            montant_tva = float(montant_tva_text)

            return formatted_date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire
        except ValueError as e:
            QMessageBox.warning(self, "Attention", str(e))
            return None
        except Exception as e:
            handle_exception(e, "Erreur lors de la récupération des données")
            return None

    def check_duplicate_expense(self, ttc, fournisseur):
        """Vérifie si une dépense avec le même montant TTC et le même fournisseur existe déjà et renvoie les doublons."""
        try:
            # Récupérer le mois et l'année actuels
            current_month = self.mois
            current_year = self.annee

            # Convertir le mois en format numérique
            month_number = convert_month_to_number(current_month)

            # Requête pour vérifier les doublons dans le mois actuel
            query_current = """
            SELECT * FROM depenses
            WHERE ttc = ? AND fournisseur = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
            """
            duplicates_current = self.db_manager.fetch_all(query_current, (ttc, fournisseur, f"{month_number:02d}", current_year))

            # Requête pour vérifier les doublons dans le mois précédent
            previous_month = month_number - 1 if month_number > 1 else 12
            previous_year = current_year if month_number > 1 else current_year - 1

            query_previous = """
            SELECT * FROM depenses
            WHERE ttc = ? AND fournisseur = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
            """
            duplicates_previous = self.db_manager.fetch_all(query_previous, (ttc, fournisseur, f"{previous_month:02d}", previous_year))

            # Combiner les doublons des deux mois
            return duplicates_current + duplicates_previous

        except Exception as e:
            handle_exception(e, "Erreur lors de la vérification des doublons")
            return []  # Retourner une liste vide en cas d'erreur

    def show_duplicate_expenses(self, duplicates):
        """Affiche les dépenses en doublon dans un tableau."""
        if not duplicates:
            QMessageBox.information(self, "Aucun doublon", "Aucun doublon trouvé.")
            return

        # Créer une nouvelle fenêtre pour afficher les doublons
        duplicate_dialog = QDialog(self)
        duplicate_dialog.setWindowTitle("Dépenses en Doublon")
        layout = QVBoxLayout(duplicate_dialog)

        # Ajouter un message d'information
        message_label = QLabel("Ces lignes existent déjà. Voulez-vous les ajouter ?")
        layout.addWidget(message_label)

        # Créer un tableau pour afficher les doublons
        table_widget = QTableWidget()
        table_widget.setColumnCount(len(TABLE_COLUMNS))
        table_widget.setHorizontalHeaderLabels(COLUMN_HEADERS)
        table_widget.setRowCount(len(duplicates))

        for row_number, row_data in enumerate(duplicates):
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row_number, column_number, item)

        layout.addWidget(table_widget)

        # Ajouter des boutons Oui et Non
        button_layout = QHBoxLayout()
        yes_button = QPushButton("Oui")
        no_button = QPushButton("Non")

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        layout.addLayout(button_layout)

        duplicate_dialog.setLayout(layout)

        # Connecter les boutons à des actions
        yes_button.clicked.connect(lambda: self.add_duplicate_expenses(duplicates, duplicate_dialog))
        no_button.clicked.connect(duplicate_dialog.reject)  # Fermer la fenêtre si Non est cliqué

        # Agrandir la fenêtre pour afficher tout le contenu
        duplicate_dialog.resize(800, 600)  # Ajustez la taille selon vos besoins

        duplicate_dialog.exec_()  # Afficher la fenêtre modale

    def add_duplicate_expenses(self, duplicates, dialog):
        """Ajoute les dépenses en doublon à la base de données."""
        for row_data in duplicates:
            # Convertir l'objet sqlite3.Row en liste
            row_data = list(row_data)  # Convertir en liste pour un accès facile
            print(f"Données de doublon : {row_data}")  # Afficher les données pour le débogage

            if len(row_data) < 7:
                QMessageBox.warning(self, "Erreur", "Les données de doublon sont incomplètes.")
                continue  # Passer à la prochaine ligne si les données sont incomplètes

            # Extraire les données nécessaires
            date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire = row_data[:7]  # Prendre seulement les 7 premiers éléments
            self.db_manager.insert_depense(date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)

        QMessageBox.information(self, "Succès", "Les doublons ont été ajoutés avec succès.")
        dialog.accept()  # Fermer la fenêtre

    def add_new_row(self):
        """Ajoute une nouvelle dépense dans la table 'depenses'."""
        if not self.validate_fields():
            return

        try:
            # Récupérer les données de la dépense
            depense_data = self._get_depense_data()
            if not depense_data:
                return

            formatted_date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire = depense_data

            # Vérifier les doublons
            duplicates = self.check_duplicate_expense(ttc, fournisseur)
            if duplicates:  # Vérifiez si des doublons existent
                self.show_duplicate_expenses(duplicates)  # Afficher les doublons
                return  # Ne pas continuer si des doublons existent

            # Vérifier si le fournisseur existe
            if not self.db_manager.fournisseur_exists(fournisseur):
                response = QMessageBox.question(self, "Fournisseur non trouvé",
                                                f"Le fournisseur '{fournisseur}' n'existe pas. Voulez-vous l'ajouter ?",
                                                QMessageBox.Yes | QMessageBox.No)
                if response == QMessageBox.Yes:
                    self.db_manager.insert_fournisseur(fournisseur)
                    configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)

            success = self.db_manager.insert_depense(*depense_data)

            if success:
                QMessageBox.information(self, "Succès", ERROR_MESSAGES["ADD_SUCCESS"])
                self.load_depenses()
                self.clear_fields()
            else:
                QMessageBox.critical(self, "Erreur", ERROR_MESSAGES["DATABASE_ERROR"])
        except Exception as e:
            handle_exception(e, "Erreur lors de l'ajout de la dépense")

    def clear_fields(self):
        """Efface tous les champs de saisie pour préparer une nouvelle entrée."""
        try:
            self.ui.lineEditDate.clear()
            self.ui.comboBoxFournisseur.setCurrentIndex(-1)
            self.ui.lineEditMontant.clear()
            self.ui.comboBoxTVA.setCurrentIndex(0)
            self.ui.lineEditMontantTVA.clear()
            self.ui.lineEditComentaire.clear()
            self.ui.checkBoxValidation.setChecked(False)

            self.selected_row_id = None
            self.ui.pushButtonValider.setEnabled(True)
        except Exception as e:
            handle_exception(e, "Erreur lors de la réinitialisation des champs")

    def load_selected_row(self, row):
        """Charge les valeurs d'une ligne sélectionnée dans les champs de saisie."""
        try:
            self.selected_row_id = self.ui.tableWidget.item(row, 0).text()
            self.ui.lineEditDate.setText(self.ui.tableWidget.item(row, 1).text())
            self.ui.comboBoxFournisseur.setCurrentText(self.ui.tableWidget.item(row, 2).text())
            self.ui.lineEditMontant.setText(self.ui.tableWidget.item(row, 3).text())
            self.ui.comboBoxTVA.setCurrentText(f"{self.ui.tableWidget.item(row, 4).text()}%")
            self.ui.lineEditMontantTVA.setText(self.ui.tableWidget.item(row, 5).text())
            self.ui.checkBoxValidation.setChecked(self.ui.tableWidget.item(row, 6).text() == "Oui")
            self.ui.lineEditComentaire.setText(self.ui.tableWidget.item(row, 7).text())

            self.ui.pushButtonValider.setEnabled(False)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la ligne sélectionnée")

    def update_row(self):
        """Modifie une dépense existante dans la base de données."""
        if not self.selected_row_id:
            QMessageBox.warning(self, "Attention", ERROR_MESSAGES["NO_SELECTION"])
            return

        if not self.validate_fields():
            return

        try:
            depense_data = self._get_depense_data()
            if not depense_data:
                return

            success = self.db_manager.update_depense(self.selected_row_id, *depense_data)

            if success:
                QMessageBox.information(self, "Succès", ERROR_MESSAGES["UPDATE_SUCCESS"])
                self.load_depenses()
                self.clear_fields()
            else:
                QMessageBox.critical(self, "Erreur", ERROR_MESSAGES["DATABASE_ERROR"])
        except Exception as e:
            handle_exception(e, "Erreur lors de la modification de la dépense")

    def delete_row(self):
        """Supprime une dépense existante de la base de données."""
        if not self.selected_row_id:
            QMessageBox.warning(self, "Attention", ERROR_MESSAGES["NO_SELECTION"])
            return

        try:
            success = self.db_manager.delete_depense(self.selected_row_id)
            if success:
                QMessageBox.information(self, "Succès", ERROR_MESSAGES["DELETE_SUCCESS"])
                self.load_depenses()
                self.clear_fields()
            else:
                QMessageBox.critical(self, "Erreur", ERROR_MESSAGES["DATABASE_ERROR"])
        except Exception as e:
            handle_exception(e, "Erreur lors de la suppression de la dépense")

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

    def calculate_and_update(self):
        """Calcule le montant TTC et met à jour les champs sans ouvrir la calculette."""
        try:
            # Récupérer le montant de la TVA
            tva_paid = float(self.ui.lineEditMontant.text())  # Montant de la TVA
            # Récupérer le taux de TVA sélectionné
            tva_rate = float(self.ui.comboBoxTVA.currentText().strip('%'))  # Taux TVA

            # Calculer le montant TTC
            ttc = tva_paid / (tva_rate / 100) + tva_paid  # Formule pour calculer le montant TTC

            # Mettre à jour les champs
            self.ui.lineEditMontantTVA.setText(f"{tva_paid:.2f}")  # Mettre à jour lineEditMontantTVA avec le montant d'entrée
            self.ui.lineEditMontant.setText(f"{ttc:.2f}")  # Mettre à jour lineEditMontant avec le montant TTC
            print(f"Montant TTC calculé: {ttc:.2f}")  # Afficher le montant TTC dans la console

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un montant valide.")