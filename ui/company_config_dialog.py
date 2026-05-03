import json
import os

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from company_config import COMPANY, reload as reload_company, _CONFIG_FILE


class CompanyConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration de l'entreprise")
        self.setModal(True)
        self.setMinimumWidth(480)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 16, 20, 16)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(8)

        self.fields = {}
        defs = [
            ("name",        "Nom affiché :"),
            ("legal",       "Dénomination légale :"),
            ("address",     "Adresse :"),
            ("postal_code", "Code postal :"),
            ("city",        "Ville :"),
            ("phone",       "Téléphone :"),
            ("email",       "Email :"),
            ("siret",       "SIRET :"),
            ("tva_intra",   "TVA intracommunautaire :"),
        ]
        for key, label in defs:
            le = QLineEdit(str(COMPANY.get(key, "")))
            self.fields[key] = le
            form.addRow(label, le)

        main_layout.addLayout(form)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #BDC3C7;")
        main_layout.addWidget(sep)

        # Logo
        logo_layout = QHBoxLayout()
        self.logo_path_edit = QLineEdit(str(COMPANY.get("logo", "")))
        self.logo_path_edit.setReadOnly(True)
        btn_browse = QPushButton("Parcourir…")
        btn_browse.clicked.connect(self._browse_logo)
        logo_layout.addWidget(self.logo_path_edit)
        logo_layout.addWidget(btn_browse)

        logo_form = QFormLayout()
        logo_form.setLabelAlignment(Qt.AlignRight)
        logo_form.addRow("Logo :", logo_layout)
        main_layout.addLayout(logo_form)

        self.logo_preview = QLabel()
        self.logo_preview.setAlignment(Qt.AlignCenter)
        self.logo_preview.setFixedHeight(80)
        self.logo_preview.setStyleSheet("border: 1px solid #BDC3C7; border-radius: 4px; background: #F8F9FA;")
        main_layout.addWidget(self.logo_preview)
        self._refresh_preview(self.logo_path_edit.text())

        # Boutons
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("color: #BDC3C7;")
        main_layout.addWidget(sep2)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_save = QPushButton("Enregistrer")
        btn_save.setDefault(True)
        btn_save.clicked.connect(self._save)
        btn_cancel = QPushButton("Annuler")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        main_layout.addLayout(btn_layout)

    def _browse_logo(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choisir un logo",
            os.path.dirname(self.logo_path_edit.text()) or ".",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if path:
            self.logo_path_edit.setText(path)
            self._refresh_preview(path)

    def _refresh_preview(self, path):
        from company_config import _BASE_DIR
        if not os.path.isabs(path):
            path = os.path.join(_BASE_DIR, path)
        pix = QPixmap(path)
        if not pix.isNull():
            self.logo_preview.setPixmap(
                pix.scaled(200, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            self.logo_preview.setText("(aucun aperçu)")

    def _save(self):
        if not self.fields["name"].text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom de l'entreprise est obligatoire.")
            return

        data = {key: le.text().strip() for key, le in self.fields.items()}
        data["logo"] = self.logo_path_edit.text().strip()
        # Conserver db_name et backup_dir existants
        data["db_name"] = COMPANY.get("db_name", "mlbdd.db")
        data["backup_dir"] = COMPANY.get("backup_dir", "data/backups")

        try:
            with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            reload_company()
            QMessageBox.information(
                self, "Enregistré",
                "Configuration sauvegardée.\n"
                "Le titre de la fenêtre et le logo seront mis à jour au prochain démarrage."
            )
            self.accept()
        except OSError as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'écrire company.json :\n{e}")
