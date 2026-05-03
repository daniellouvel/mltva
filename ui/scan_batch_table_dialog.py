"""
Dialogue de scan multi-factures en mode tableau :
toutes les factures sont scannees au demarrage puis affichees dans un
tableau editable. L utilisateur coche les lignes a enregistrer, peut
modifier les valeurs detectees, et valide tout d un coup.

Alternative au ScanBatchDialog (mode sequentiel) — les deux coexistent
et l utilisateur choisit a chaque import.
"""

import os
from datetime import datetime

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox, QCheckBox, QWidget,
    QHeaderView, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from constants import UI_CONFIG
from util import calculate_tva
from scan_facture import scan_facture
from ui.async_worker import run_with_progress


COL_CHECK = 0
COL_FICHIER = 1
COL_DATE = 2
COL_FOURNISSEUR = 3
COL_TTC = 4
COL_TVA = 5
COL_MONTANT_TVA = 6
COL_VALIDATION = 7
COL_COMMENTAIRE = 8

HEADERS = ["✓", "Fichier", "Date", "Fournisseur", "TTC",
           "Taux TVA", "Montant TVA", "Validé", "Commentaire"]


def _scan_all(file_paths, selected_month, selected_year):
    """
    Scanne tous les fichiers en sequence. Retourne une liste de dicts :
    {file: str, ok: bool, error: str|None, date, fournisseur, ttc, tva, montant_tva}
    Les dates hors periode sont remplacees par 01/MM/YYYY (la confirmation
    interactive du mode sequentiel n a pas de sens en mode batch tableau).
    """
    results = []
    for path in file_paths:
        item = {"file": path, "ok": False, "error": None,
                "date": "", "fournisseur": "", "ttc": "", "tva": "20.00%",
                "montant_tva": "", "valide": False, "commentaire": ""}
        try:
            r = scan_facture(path)
            item["ok"] = True
            item["fournisseur"] = r.get("fournisseur", "")
            item["ttc"] = r.get("montant", "")
            item["tva"] = r.get("tva_rate") or "20.00%"
            item["commentaire"] = ""

            # Date : ajustement auto a la periode active si hors mois/annee
            date_str = r.get("date", "")
            if date_str:
                try:
                    d = datetime.strptime(date_str, "%d/%m/%Y")
                    if d.month != selected_month or d.year != selected_year:
                        item["date"] = f"01/{selected_month:02d}/{selected_year}"
                    else:
                        item["date"] = date_str
                except ValueError:
                    item["date"] = date_str
            else:
                item["date"] = f"01/{selected_month:02d}/{selected_year}"

            # Pre-calcul du montant TVA
            mt = calculate_tva(item["ttc"], item["tva"])
            item["montant_tva"] = f"{mt:.2f}" if mt is not None else ""
        except Exception as e:
            item["error"] = str(e)
        results.append(item)
    return results


class ScanBatchTableDialog(QDialog):
    def __init__(self, file_paths, db_manager, mois, annee,
                 selected_month, selected_year, parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self.db_manager = db_manager
        self.mois = mois
        self.annee = annee
        self.selected_month = selected_month
        self.selected_year = selected_year

        self.setWindowTitle(f"Scan factures — vue tableau ({len(file_paths)} fichier(s))")
        self.resize(1200, 600)
        self.setModal(True)

        self._setup_ui()
        self._scan_and_fill()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "Modifiez les cellules si nécessaire, cochez les factures à enregistrer "
            "puis cliquez sur «Enregistrer les lignes cochées».\n"
            "Les lignes en rouge n'ont pas pu être scannées correctement et seront ignorées."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        self.table = QTableWidget()
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.cellChanged.connect(self._on_cell_changed)

        h = self.table.horizontalHeader()
        h.setSectionResizeMode(COL_CHECK, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_FICHIER, QHeaderView.Interactive)
        h.setSectionResizeMode(COL_FOURNISSEUR, QHeaderView.Stretch)
        h.setSectionResizeMode(COL_COMMENTAIRE, QHeaderView.Stretch)
        layout.addWidget(self.table, stretch=1)

        # Boutons groupés
        btn_layout = QHBoxLayout()
        btn_check_all = QPushButton("Tout cocher")
        btn_check_all.setObjectName("pushButtonModifier")
        btn_uncheck_all = QPushButton("Tout décocher")
        btn_uncheck_all.setObjectName("pushButtonEffacer")
        btn_layout.addWidget(btn_check_all)
        btn_layout.addWidget(btn_uncheck_all)
        btn_layout.addStretch()

        self.btn_save = QPushButton("Enregistrer les lignes cochées")
        self.btn_save.setObjectName("pushButtonValider")
        btn_cancel = QPushButton("Fermer")
        btn_cancel.setObjectName("pushButtonSupprimer")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        btn_check_all.clicked.connect(lambda: self._set_all_checked(True))
        btn_uncheck_all.clicked.connect(lambda: self._set_all_checked(False))
        self.btn_save.clicked.connect(self._on_save)
        btn_cancel.clicked.connect(self.reject)

    # ── Population du tableau ─────────────────────────────────────────────────

    def _scan_and_fill(self):
        """Scanne tous les fichiers (en thread) puis remplit le tableau."""
        worker_res = run_with_progress(
            parent=self,
            title="Scan OCR",
            message=f"Analyse de {len(self.file_paths)} facture(s) ...\n"
                    "(cela peut prendre plusieurs secondes par PDF)",
            target=_scan_all,
            args=(self.file_paths, self.selected_month, self.selected_year),
        )
        if not worker_res.success:
            QMessageBox.critical(self, "Erreur scan", str(worker_res.error))
            self.reject()
            return

        results = worker_res.value
        self.table.blockSignals(True)
        self.table.setRowCount(len(results))
        for row, item in enumerate(results):
            self._populate_row(row, item)
        self.table.blockSignals(False)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(COL_FOURNISSEUR, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(COL_COMMENTAIRE, QHeaderView.Stretch)

    def _populate_row(self, row, item):
        # Checkbox cochee par defaut si scan OK
        chk = QCheckBox()
        chk.setChecked(item["ok"])
        chk.setEnabled(item["ok"])
        wrap = QWidget()
        lay = QHBoxLayout(wrap)
        lay.addWidget(chk)
        lay.setAlignment(Qt.AlignCenter)
        lay.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row, COL_CHECK, wrap)
        wrap.setProperty("checkbox", chk)

        # Fichier (read-only)
        f_item = QTableWidgetItem(os.path.basename(item["file"]))
        f_item.setFlags(f_item.flags() & ~Qt.ItemIsEditable)
        f_item.setToolTip(item["file"])
        self.table.setItem(row, COL_FICHIER, f_item)

        # Date / Fournisseur / TTC / Commentaire : editables
        self.table.setItem(row, COL_DATE, QTableWidgetItem(item["date"]))
        self.table.setItem(row, COL_FOURNISSEUR, QTableWidgetItem(item["fournisseur"]))
        self.table.setItem(row, COL_TTC, QTableWidgetItem(item["ttc"]))
        self.table.setItem(row, COL_COMMENTAIRE, QTableWidgetItem(item["commentaire"]))

        # TVA : combobox
        cb_tva = QComboBox()
        cb_tva.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])
        idx = cb_tva.findText(item["tva"])
        if idx >= 0:
            cb_tva.setCurrentIndex(idx)
        cb_tva.currentTextChanged.connect(lambda _t, r=row: self._recalc_montant_tva(r))
        self.table.setCellWidget(row, COL_TVA, cb_tva)

        # Montant TVA : read-only, calcule
        mt_item = QTableWidgetItem(item["montant_tva"])
        mt_item.setFlags(mt_item.flags() & ~Qt.ItemIsEditable)
        mt_item.setBackground(QColor("#D6EAF8"))
        self.table.setItem(row, COL_MONTANT_TVA, mt_item)

        # Validation : combobox Oui/Non
        cb_val = QComboBox()
        cb_val.addItems(["Non", "Oui"])
        cb_val.setCurrentIndex(1 if item["valide"] else 0)
        self.table.setCellWidget(row, COL_VALIDATION, cb_val)

        # Coloration des lignes en erreur
        if not item["ok"]:
            color = QColor("#FADBD8")
            for col in range(self.table.columnCount()):
                cell = self.table.item(row, col)
                if cell:
                    cell.setBackground(color)
            err_item = self.table.item(row, COL_FICHIER)
            err_item.setToolTip(f"Erreur scan : {item['error']}\n{item['file']}")

    # ── Logique ───────────────────────────────────────────────────────────────

    def _on_cell_changed(self, row, col):
        """Recalcule le montant TVA si TTC change."""
        if col == COL_TTC:
            self._recalc_montant_tva(row)

    def _recalc_montant_tva(self, row):
        ttc_item = self.table.item(row, COL_TTC)
        cb_tva = self.table.cellWidget(row, COL_TVA)
        if ttc_item is None or cb_tva is None:
            return
        result = calculate_tva(ttc_item.text(), cb_tva.currentText())
        text = f"{result:.2f}" if result is not None else ""
        mt_item = self.table.item(row, COL_MONTANT_TVA)
        if mt_item is not None:
            mt_item.setText(text)

    def _set_all_checked(self, checked: bool):
        for row in range(self.table.rowCount()):
            wrap = self.table.cellWidget(row, COL_CHECK)
            if wrap:
                cb = wrap.property("checkbox")
                if cb and cb.isEnabled():
                    cb.setChecked(checked)

    def _is_row_checked(self, row):
        wrap = self.table.cellWidget(row, COL_CHECK)
        if not wrap:
            return False
        cb = wrap.property("checkbox")
        return cb is not None and cb.isChecked()

    def _read_row(self, row):
        """Retourne (date_text, fournisseur, ttc_text, tva_text, montant_tva_text, validation, commentaire)."""
        date_text = (self.table.item(row, COL_DATE) or QTableWidgetItem("")).text().strip()
        fournisseur = (self.table.item(row, COL_FOURNISSEUR) or QTableWidgetItem("")).text().strip()
        ttc_text = (self.table.item(row, COL_TTC) or QTableWidgetItem("")).text().strip()
        cb_tva = self.table.cellWidget(row, COL_TVA)
        tva_text = cb_tva.currentText() if cb_tva else ""
        mt_text = (self.table.item(row, COL_MONTANT_TVA) or QTableWidgetItem("")).text().strip()
        cb_val = self.table.cellWidget(row, COL_VALIDATION)
        validation = cb_val.currentText() if cb_val else "Non"
        commentaire = (self.table.item(row, COL_COMMENTAIRE) or QTableWidgetItem("")).text().strip()
        return date_text, fournisseur, ttc_text, tva_text, mt_text, validation, commentaire

    def _on_save(self):
        cochees = [r for r in range(self.table.rowCount()) if self._is_row_checked(r)]
        if not cochees:
            QMessageBox.warning(self, "Aucune sélection",
                                "Aucune ligne cochée. Cochez au moins une facture à enregistrer.")
            return

        rep = QMessageBox.question(
            self, "Confirmation",
            f"Enregistrer {len(cochees)} facture(s) cochée(s) ?\n\n"
            "Les doublons seront detectés et confirmés un par un.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if rep != QMessageBox.Yes:
            return

        nb_ok = 0
        nb_skipped_invalid = 0
        nb_skipped_duplicate = 0
        nb_errors = 0

        for row in cochees:
            data = self._read_row(row)
            date_text, fournisseur, ttc_text, tva_text, mt_text, validation, commentaire = data

            if not all([date_text, fournisseur, ttc_text]):
                nb_skipped_invalid += 1
                continue
            try:
                date_obj = datetime.strptime(date_text, "%d/%m/%Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                ttc = float(ttc_text)
                tva_rate = float(tva_text.strip('%'))
                montant_tva = float(mt_text) if mt_text else 0.0
            except ValueError:
                nb_skipped_invalid += 1
                continue

            doublons = self.db_manager.find_depense_doublons(
                ttc, fournisseur, date_obj.month, date_obj.year
            )
            if doublons:
                rep = QMessageBox.question(
                    self, "Doublon détecté",
                    f"Ligne {row + 1} :\n"
                    f"  {fournisseur} — {ttc:.2f} € — {date_text}\n"
                    f"existe déjà.\n\nL'ajouter quand même ?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if rep != QMessageBox.Yes:
                    nb_skipped_duplicate += 1
                    continue

            success = self.db_manager.insert_depense_with_fournisseur(
                formatted_date, fournisseur, ttc, tva_rate, montant_tva, validation, commentaire
            )
            if success:
                nb_ok += 1
            else:
                nb_errors += 1

        msg = (f"Traitement terminé.\n\n"
               f"  {nb_ok} facture(s) enregistrée(s)\n"
               f"  {nb_skipped_invalid} ignorée(s) (données invalides)\n"
               f"  {nb_skipped_duplicate} ignorée(s) (doublon refusé)\n")
        if nb_errors:
            msg += f"  {nb_errors} erreur(s) base de données\n"
        QMessageBox.information(self, "Résumé", msg)
        self.accept()
