import os
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton,
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt

from constants import UI_CONFIG
from util import calculate_tva, configure_fournisseur_combobox
from scan_facture import scan_facture


class ScanBatchDialog(QDialog):
    """Dialogue de scan séquentiel pour un lot de factures."""

    def __init__(self, file_paths, db_manager, mois, annee,
                 selected_month, selected_year, parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self.db_manager = db_manager
        self.mois = mois
        self.annee = annee
        self.selected_month = selected_month
        self.selected_year = selected_year

        self.current_index = 0
        self.validated_count = 0
        self.skipped_count = 0
        self.errors = []

        self.setWindowTitle("Scan de factures — traitement par lot")
        self.setMinimumWidth(620)
        self.setModal(True)

        self._setup_ui()
        self._process_next()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Progression
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-weight:bold; font-size:11pt;")
        self.filename_label = QLabel()
        self.filename_label.setStyleSheet("color:#2C5F8A; font-style:italic;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.file_paths))

        layout.addWidget(self.progress_label)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.progress_bar)

        # Formulaire
        group = QGroupBox("Données détectées — modifiables avant validation")
        grid = QGridLayout(group)

        self.edit_date = QLineEdit()
        self.edit_date.setPlaceholderText("JJ/MM/AAAA")

        self.combo_fournisseur = QComboBox()
        configure_fournisseur_combobox(self.combo_fournisseur, self.db_manager)

        self.edit_montant = QLineEdit()
        self.edit_montant.setPlaceholderText("0.00")

        self.combo_tva = QComboBox()
        self.combo_tva.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])

        self.edit_montant_tva = QLineEdit()
        self.edit_montant_tva.setReadOnly(True)
        self.edit_montant_tva.setObjectName("lineEditmontanttva")

        self.edit_commentaire = QLineEdit()
        self.check_validation = QCheckBox("Validé")

        grid.addWidget(QLabel("Date :"), 0, 0)
        grid.addWidget(self.edit_date, 0, 1)
        grid.addWidget(QLabel("Fournisseur :"), 1, 0)
        grid.addWidget(self.combo_fournisseur, 1, 1)
        grid.addWidget(QLabel("TTC :"), 2, 0)
        grid.addWidget(self.edit_montant, 2, 1)
        grid.addWidget(QLabel("Taux TVA :"), 3, 0)
        grid.addWidget(self.combo_tva, 3, 1)
        grid.addWidget(QLabel("Montant TVA :"), 4, 0)
        grid.addWidget(self.edit_montant_tva, 4, 1)
        grid.addWidget(QLabel("Commentaire :"), 5, 0)
        grid.addWidget(self.edit_commentaire, 5, 1)
        grid.addWidget(self.check_validation, 6, 1)

        layout.addWidget(group)

        self.edit_montant.textChanged.connect(self._recalc_tva)
        self.combo_tva.currentTextChanged.connect(self._recalc_tva)

        # Boutons
        btn_layout = QHBoxLayout()
        self.btn_valider = QPushButton("Valider")
        self.btn_valider.setObjectName("pushButtonValider")
        self.btn_passer = QPushButton("Passer")
        self.btn_passer.setObjectName("pushButtonEffacer")
        self.btn_arreter = QPushButton("Arrêter")
        self.btn_arreter.setObjectName("pushButtonSupprimer")

        btn_layout.addWidget(self.btn_valider)
        btn_layout.addWidget(self.btn_passer)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_arreter)
        layout.addLayout(btn_layout)

        self.btn_valider.clicked.connect(self._on_valider)
        self.btn_passer.clicked.connect(self._on_passer)
        self.btn_arreter.clicked.connect(self._on_arreter)

    # ── Logique ───────────────────────────────────────────────────────────────

    def _recalc_tva(self):
        result = calculate_tva(self.edit_montant.text(), self.combo_tva.currentText())
        self.edit_montant_tva.setText(f"{result:.2f}" if result is not None else "")

    def _clear_form(self):
        self.edit_date.clear()
        self.combo_fournisseur.setCurrentIndex(-1)
        self.edit_montant.clear()
        self.combo_tva.setCurrentIndex(2)   # 20.00% par défaut
        self.edit_montant_tva.clear()
        self.edit_commentaire.clear()
        self.check_validation.setChecked(False)

    def _process_next(self):
        if self.current_index >= len(self.file_paths):
            self._show_summary()
            return

        file_path = self.file_paths[self.current_index]
        n = self.current_index + 1
        total = len(self.file_paths)
        self.progress_bar.setValue(self.current_index)
        self.progress_label.setText(f"Facture {n} sur {total}")
        self.filename_label.setText(os.path.basename(file_path))
        self._clear_form()

        try:
            result = scan_facture(file_path)
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Tesseract manquant", str(e))
            self._show_summary()
            return
        except Exception as e:
            self.errors.append(f"{os.path.basename(file_path)} : {e}")
            QMessageBox.warning(
                self, "Erreur scan",
                f"Impossible de scanner :\n{os.path.basename(file_path)}\n\n{e}\n\n"
                "Saisissez manuellement ou cliquez sur Passer."
            )
            return

        # Ajustement de la date si hors période
        date_a_utiliser = result.get("date", "")
        if date_a_utiliser:
            try:
                date_obj = datetime.strptime(date_a_utiliser, "%d/%m/%Y")
                if (date_obj.month != self.selected_month
                        or date_obj.year != self.selected_year):
                    date_periode = f"01/{self.selected_month:02d}/{self.selected_year}"
                    rep = QMessageBox.question(
                        self, "Période différente",
                        f"La date de la facture ({date_a_utiliser}) ne correspond pas\n"
                        f"à la période active ({self.mois} {self.annee}).\n\n"
                        f"Utiliser la date {date_periode} (période active) ?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
                    if rep == QMessageBox.Yes:
                        date_a_utiliser = date_periode
            except ValueError:
                pass

        if result.get("tva_rate"):
            self.combo_tva.setCurrentText(result["tva_rate"])
        if date_a_utiliser:
            self.edit_date.setText(date_a_utiliser)
        if result.get("fournisseur"):
            self.combo_fournisseur.setEditText(result["fournisseur"])
        if result.get("montant"):
            self.edit_montant.setText(result["montant"])
        self._recalc_tva()

    def _on_valider(self):
        date_text = self.edit_date.text().strip()
        fournisseur = self.combo_fournisseur.currentText().strip()
        montant_text = self.edit_montant.text().strip()
        tva_text = self.combo_tva.currentText()
        montant_tva_text = self.edit_montant_tva.text().strip()
        validation = "Oui" if self.check_validation.isChecked() else "Non"
        commentaire = self.edit_commentaire.text().strip()

        if not all([date_text, fournisseur, montant_text]):
            QMessageBox.warning(self, "Champs manquants",
                                "Date, Fournisseur et TTC sont obligatoires.")
            return

        try:
            date_obj = datetime.strptime(date_text, "%d/%m/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            ttc = float(montant_text)
            tva_rate = float(tva_text.strip('%'))
            montant_tva = float(montant_tva_text) if montant_tva_text else 0.0
        except ValueError as e:
            QMessageBox.warning(self, "Données invalides", str(e))
            return

        # Vérification des doublons (même TTC + fournisseur, même mois)
        doublons = self.db_manager.find_depense_doublons(
            ttc, fournisseur, date_obj.month, date_obj.year
        )
        if doublons:
            mois_annee = date_obj.strftime("%m/%Y")
            rep = QMessageBox.question(
                self, "Doublon détecté",
                f"Une dépense identique existe déjà pour {mois_annee} :\n"
                f"  Fournisseur : {fournisseur}\n"
                f"  Montant TTC : {ttc:.2f} €\n\n"
                "Voulez-vous l'enregistrer quand même ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if rep != QMessageBox.Yes:
                return

        # Insertion atomique : fournisseur (si absent) + dépense en une seule transaction
        success = self.db_manager.insert_depense_with_fournisseur(
            formatted_date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire
        )
        if not success:
            QMessageBox.critical(self, "Erreur base de données",
                                 "Impossible d'enregistrer la dépense.")
            return

        self.validated_count += 1
        self.current_index += 1
        self._process_next()

    def _on_passer(self):
        self.skipped_count += 1
        self.current_index += 1
        self._process_next()

    def _on_arreter(self):
        remaining = len(self.file_paths) - self.current_index
        rep = QMessageBox.question(
            self, "Arrêter le traitement",
            f"Arrêter maintenant ? {remaining} facture(s) restante(s) non traitée(s).",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self._show_summary()

    def _show_summary(self):
        self.progress_bar.setValue(len(self.file_paths))
        non_traites = len(self.file_paths) - self.current_index
        summary = (
            f"Traitement terminé.\n\n"
            f"  {self.validated_count} facture(s) enregistrée(s)\n"
            f"  {self.skipped_count} facture(s) passée(s)\n"
        )
        if non_traites > 0:
            summary += f"  {non_traites} facture(s) non traitée(s) (arrêt anticipé)\n"
        if self.errors:
            summary += f"\n{len(self.errors)} erreur(s) de scan :\n"
            summary += "\n".join(f"  • {e}" for e in self.errors)
        QMessageBox.information(self, "Résumé du traitement", summary)
        self.accept()
