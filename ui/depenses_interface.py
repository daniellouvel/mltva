from PySide6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QVBoxLayout, QTableWidget, QLabel, QHBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Qt, QEvent, QDate
from ui.ui_gestion_depenses import Ui_Dialog
from ui.base_gestion import GestionBase
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
from calculette import CalculetteDialog
from scan_facture import scan_facture
from scan_email import load_email_config, fetch_invoice_pdfs
from ui.scan_batch_dialog import ScanBatchDialog
from ui.email_config_dialog import EmailConfigDialog
from ui.async_worker import run_with_progress

TABLE_COLUMNS = {
    "REPERE": 0,
    "DATE": 1,
    "FOURNISSEUR": 2,
    "TTC": 3,
    "TVA_RATE": 4,
    "TVA_AMOUNT": 5,
    "VALIDATION": 6,
    "COMMENTAIRE": 7,
}

COLUMN_WIDTHS = {
    TABLE_COLUMNS["REPERE"]: 50,
    TABLE_COLUMNS["DATE"]: 100,
    TABLE_COLUMNS["FOURNISSEUR"]: 185,
    TABLE_COLUMNS["TTC"]: 80,
    TABLE_COLUMNS["TVA_RATE"]: 80,
    TABLE_COLUMNS["TVA_AMOUNT"]: 100,
    TABLE_COLUMNS["VALIDATION"]: 80,
    TABLE_COLUMNS["COMMENTAIRE"]: 400,
}

COLUMN_HEADERS = ["Repère", "Date", "Fournisseur", "TTC", "Taux TVA", "Montant TVA", "Validation", "Commentaire"]


class GestionDepenses(GestionBase):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.selected_row_id = None
        self.periode_manager = PeriodeManager()
        self.mois, self.annee = self.periode_manager.get_periode()
        self.db_manager = DatabaseManager()

        self._setup_ui()
        self.load_periode()
        self.load_depenses()
        self.ui.lineEditDate.setFocus()

    def _setup_ui(self):
        self.configure_table()
        self.ui.calendarWidget.setVisible(UI_CONFIG["CALENDAR_VISIBLE"])
        self.ui.lineEditDate.mousePressEvent = self.show_calendar_on_focus
        self.ui.calendarWidget.clicked.connect(self.on_calendar_date_clicked)
        self.ui.lineEditDate.clear()
        configure_fournisseur_combobox(self.ui.comboBoxFournisseur, self.db_manager)
        self.ui.comboBoxTVA.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])
        self._connect_buttons()
        self.ui.lineEditMontant.textChanged.connect(self.calculate_tva)
        self.ui.comboBoxTVA.currentTextChanged.connect(self.calculate_tva)
        self.ui.tableWidget.cellClicked.connect(self.load_selected_row)
        self.ui.push_calculettettc.clicked.connect(self.calculate_and_update)
        self.ui.push_scan_facture.clicked.connect(self.on_scan_facture)
        self.ui.push_import_email.clicked.connect(self.on_import_email)
        self.ui.pushButtonValider.setDefault(True)
        self.ui.quitterButton.setAutoDefault(False)
        self.ui.quitterButton.setDefault(False)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.installEventFilter(self)
        self.ui.lineEditMontantTVA.setReadOnly(True)

    def _connect_buttons(self):
        button_connections = {
            "quitterButton": self.close,
            "pushButtonValider": self.add_new_row,
            "pushButtonModifier": self.update_row,
            "pushButtonSupprimer": self.delete_row,
            "pushButtonEffacer": self.clear_fields,
        }
        for button_name, callback in button_connections.items():
            if hasattr(self.ui, button_name):
                getattr(self.ui, button_name).clicked.connect(callback)
            else:
                print(f"Erreur : Le bouton '{button_name}' n'existe pas dans le fichier .ui.")

    def configure_table(self):
        try:
            self.ui.tableWidget.setColumnCount(len(COLUMN_HEADERS))
            self.ui.tableWidget.setHorizontalHeaderLabels(COLUMN_HEADERS)
            self.ui.tableWidget.verticalHeader().setVisible(False)
            self.set_column_widths()
        except Exception as e:
            handle_exception(e, "Erreur lors de la configuration du tableau")

    def set_column_widths(self):
        try:
            for col, width in COLUMN_WIDTHS.items():
                self.ui.tableWidget.setColumnWidth(col, width)
        except Exception as e:
            handle_exception(e, "Erreur lors de la définition des largeurs de colonnes")

    def load_periode(self):
        try:
            self.ui.moisLabel.setText(self.mois)
            self.ui.anneeLabel.setText(str(self.annee))
            self.selected_month = convert_month_to_number(self.mois)
            self.selected_year = int(self.annee)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la période")

    def load_depenses(self):
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
                            data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
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
        try:
            self.ui.lineEdittotalttc.setText(f"{total_ttc:.2f}")
            self.ui.lineEditmontanttva.setText(f"{total_montant_tva:.2f}")
        except Exception as e:
            handle_exception(e, "Erreur lors de la mise à jour des totaux")

    def validate_fields(self):
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
        try:
            date_text = self.ui.lineEditDate.text()
            fournisseur = self.ui.comboBoxFournisseur.currentText()
            ttc_text = self.ui.lineEditMontant.text()
            tva_rate_text = self.ui.comboBoxTVA.currentText()
            montant_tva_text = self.ui.lineEditMontantTVA.text()
            commentaire = self.ui.lineEditCommentaire.text()
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
        try:
            month_number = convert_month_to_number(self.mois)
            query = """
            SELECT * FROM depenses
            WHERE ttc = ? AND fournisseur = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
            """
            duplicates_current = self.db_manager.fetch_all(query, (ttc, fournisseur, f"{month_number:02d}", self.annee))
            previous_month = month_number - 1 if month_number > 1 else 12
            annee_int = int(self.annee)
            previous_year = annee_int if month_number > 1 else annee_int - 1
            duplicates_previous = self.db_manager.fetch_all(query, (ttc, fournisseur, f"{previous_month:02d}", previous_year))
            return duplicates_current + duplicates_previous
        except Exception as e:
            handle_exception(e, "Erreur lors de la vérification des doublons")
            return []

    def show_duplicate_expenses(self, duplicates):
        if not duplicates:
            QMessageBox.information(self, "Aucun doublon", "Aucun doublon trouvé.")
            return
        duplicate_dialog = QDialog(self)
        duplicate_dialog.setWindowTitle("Dépenses en Doublon")
        layout = QVBoxLayout(duplicate_dialog)
        layout.addWidget(QLabel("Ces lignes existent déjà. Voulez-vous les ajouter ?"))
        table_widget = QTableWidget()
        table_widget.setColumnCount(len(TABLE_COLUMNS))
        table_widget.setHorizontalHeaderLabels(COLUMN_HEADERS)
        table_widget.setRowCount(len(duplicates))
        for row_number, row_data in enumerate(duplicates):
            for column_number, data in enumerate(row_data):
                table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        layout.addWidget(table_widget)
        button_layout = QHBoxLayout()
        yes_button = QPushButton("Oui")
        no_button = QPushButton("Non")
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        layout.addLayout(button_layout)
        yes_button.clicked.connect(lambda: self.add_duplicate_expenses(duplicates, duplicate_dialog))
        no_button.clicked.connect(duplicate_dialog.reject)
        duplicate_dialog.resize(800, 600)
        duplicate_dialog.exec()

    def add_duplicate_expenses(self, duplicates, dialog):
        for row_data in duplicates:
            row_data = list(row_data)
            if len(row_data) < 8:
                QMessageBox.warning(self, "Erreur", "Les données de doublon sont incomplètes.")
                continue
            date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire = row_data[1:8]
            self.db_manager.insert_depense(date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)
        QMessageBox.information(self, "Succès", "Les doublons ont été ajoutés avec succès.")
        dialog.accept()

    def add_new_row(self):
        if not self.validate_fields():
            return
        try:
            depense_data = self._get_depense_data()
            if not depense_data:
                return
            formatted_date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire = depense_data
            duplicates = self.check_duplicate_expense(ttc, fournisseur)
            if duplicates:
                self.show_duplicate_expenses(duplicates)
                return
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
        try:
            self.ui.lineEditDate.clear()
            self.ui.comboBoxFournisseur.setCurrentIndex(-1)
            self.ui.lineEditMontant.clear()
            self.ui.comboBoxTVA.setCurrentIndex(0)
            self.ui.lineEditMontantTVA.clear()
            self.ui.lineEditCommentaire.clear()
            self.ui.checkBoxValidation.setChecked(False)
            self.selected_row_id = None
            self.ui.pushButtonValider.setEnabled(True)
        except Exception as e:
            handle_exception(e, "Erreur lors de la réinitialisation des champs")

    def load_selected_row(self, row):
        try:
            self.selected_row_id = self.ui.tableWidget.item(row, 0).text()
            self.ui.lineEditDate.setText(self.ui.tableWidget.item(row, 1).text())
            self.ui.comboBoxFournisseur.setCurrentText(self.ui.tableWidget.item(row, 2).text())
            self.ui.lineEditMontant.setText(self.ui.tableWidget.item(row, 3).text())
            self.ui.comboBoxTVA.setCurrentText(f"{self.ui.tableWidget.item(row, 4).text()}%")
            self.ui.lineEditMontantTVA.setText(self.ui.tableWidget.item(row, 5).text())
            self.ui.checkBoxValidation.setChecked(self.ui.tableWidget.item(row, 6).text() == "Oui")
            self.ui.lineEditCommentaire.setText(self.ui.tableWidget.item(row, 7).text())
            self.ui.pushButtonValider.setEnabled(False)
        except Exception as e:
            handle_exception(e, "Erreur lors du chargement de la ligne sélectionnée")

    def update_row(self):
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
        if not self.selected_row_id:
            QMessageBox.warning(self, "Attention", ERROR_MESSAGES["NO_SELECTION"])
            return
        try:
            row = self.ui.tableWidget.currentRow()
            confirmation_message = (
                f"Êtes-vous sûr de vouloir supprimer cette dépense ?\n\n"
                f"Date : {self.ui.tableWidget.item(row, 1).text()}\n"
                f"Fournisseur : {self.ui.tableWidget.item(row, 2).text()}\n"
                f"Montant : {self.ui.tableWidget.item(row, 3).text()}"
            )
            reply = QMessageBox.question(self, "Confirmation de suppression", confirmation_message,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.db_manager.delete_depense(self.selected_row_id)
                if success:
                    QMessageBox.information(self, "Succès", ERROR_MESSAGES["DELETE_SUCCESS"])
                    self.load_depenses()
                    self.clear_fields()
                else:
                    QMessageBox.critical(self, "Erreur", ERROR_MESSAGES["DATABASE_ERROR"])
        except Exception as e:
            handle_exception(e, "Erreur lors de la suppression de la dépense")

    def on_scan_facture(self):
        """Scan d'une ou plusieurs factures (sélection multiple)."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionner une ou plusieurs factures",
            "", "Factures (*.pdf *.png *.jpg *.jpeg *.tif *.tiff);;Tous (*)"
        )
        if not file_paths:
            return

        if len(file_paths) == 1:
            self._scan_single(file_paths[0])
        else:
            self._scan_batch(file_paths)

    def _scan_single(self, file_path):
        """Scan d'une facture unique : pré-remplit le formulaire principal."""
        worker_res = run_with_progress(
            parent=self,
            title="Scan OCR",
            message=f"Analyse de la facture ...",
            target=scan_facture,
            args=(file_path,),
        )
        if not worker_res.success:
            err = worker_res.error
            if isinstance(err, FileNotFoundError):
                QMessageBox.critical(self, "Tesseract manquant", str(err))
            else:
                handle_exception(err, "Erreur lors du scan de la facture")
            return
        result = worker_res.value
        try:
            champs_trouves = [k for k, v in result.items() if v and k != "texte_brut"]
            if not champs_trouves:
                QMessageBox.warning(
                    self, "Scan incomplet",
                    "Aucun champ n'a pu être extrait automatiquement.\n"
                    "Vérifiez la qualité de l'image et remplissez manuellement."
                )
                return

            date_a_utiliser = result["date"]
            if result["date"]:
                try:
                    date_obj = datetime.strptime(result["date"], "%d/%m/%Y")
                    if date_obj.month != self.selected_month or date_obj.year != self.selected_year:
                        date_periode = f"01/{self.selected_month:02d}/{self.selected_year}"
                        reponse = QMessageBox.question(
                            self, "Période différente",
                            f"La date de la facture ({result['date']}) ne correspond pas "
                            f"à la période active ({self.mois} {self.annee}).\n\n"
                            f"Voulez-vous enregistrer cette dépense en {self.mois} {self.annee} "
                            f"(date : {date_periode}) ?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.Yes
                        )
                        if reponse == QMessageBox.Yes:
                            date_a_utiliser = date_periode
                except ValueError:
                    pass

            if result["tva_rate"]:
                self.ui.comboBoxTVA.setCurrentText(result["tva_rate"])
            if date_a_utiliser:
                self.ui.lineEditDate.setText(date_a_utiliser)
            if result["fournisseur"]:
                self.ui.comboBoxFournisseur.setEditText(result["fournisseur"])
            if result["montant"]:
                self.ui.lineEditMontant.setText(result["montant"])
            self.calculate_tva()

            QMessageBox.information(
                self, "Scan terminé",
                f"Champs détectés : {', '.join(champs_trouves)}\n\n"
                "Vérifiez les valeurs puis cliquez sur Valider pour enregistrer."
            )
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Tesseract manquant", str(e))
        except Exception as e:
            handle_exception(e, "Erreur lors du scan de la facture")

    def _scan_batch(self, file_paths):
        """Scan de plusieurs factures via le dialogue de traitement par lot."""
        dlg = ScanBatchDialog(
            file_paths, self.db_manager,
            self.mois, self.annee,
            self.selected_month, self.selected_year,
            parent=self
        )
        dlg.exec()
        self.load_depenses()

    def on_import_email(self):
        """Importe les factures PDF reçues par email puis lance le traitement par lot."""
        cfg = load_email_config()

        if not cfg.get("email") or not cfg.get("password"):
            rep = QMessageBox.question(
                self, "Configuration manquante",
                "L'accès email n'est pas encore configuré.\n\n"
                "Voulez-vous configurer la connexion maintenant ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if rep != QMessageBox.Yes:
                return
            dlg = EmailConfigDialog(self)
            if dlg.exec() != EmailConfigDialog.Accepted:
                return
            cfg = load_email_config()

        # Connexion IMAP + telechargement dans un QThread (UI reactive)
        result = run_with_progress(
            parent=self,
            title="Connexion IMAP",
            message=f"Recuperation des emails de {cfg['email']}\n"
                    f"(derniers {cfg['jours']} jours) ...",
            target=fetch_invoice_pdfs,
            args=(cfg["server"], cfg["port"], cfg["email"], cfg["password"],
                  cfg.get("dossier", "INBOX"), cfg.get("jours", 30)),
        )
        if not result.success:
            QMessageBox.critical(self, "Erreur email",
                                 f"Impossible de récupérer les emails :\n\n{result.error}")
            return
        pdf_paths, nb_emails = result.value

        if not pdf_paths:
            QMessageBox.information(
                self, "Aucune pièce jointe",
                f"{nb_emails} email(s) analysé(s) — aucun PDF trouvé."
            )
            return

        rep = QMessageBox.question(
            self, "Factures trouvées",
            f"{nb_emails} email(s) analysé(s).\n"
            f"{len(pdf_paths)} PDF trouvé(s).\n\n"
            "Lancer le traitement par lot ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self._scan_batch(pdf_paths)
