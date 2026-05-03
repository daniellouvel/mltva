from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from company_config import COMPANY, get_logo_path
from version import APP_VERSION, APP_NAME

# Informations développeur — non modifiables
_DEV = {
    "name":    "Daniel Louvel",
    "address": "30 route du Carouge",
    "city":    "76430 Sandouville",
    "phone":   "06 70 86 24 84",
    "email":   "daniel.louvel@orange.fr",
}


def _separator(parent_layout):
    sep = QFrame()
    sep.setFrameShape(QFrame.HLine)
    sep.setStyleSheet("color: #D5D8DC; margin: 4px 0;")
    parent_layout.addWidget(sep)


def _section_title(text):
    lbl = QLabel(text.upper())
    lbl.setStyleSheet("color: #95A5A6; font-size: 8pt; font-weight: bold; letter-spacing: 1px;")
    return lbl


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"À propos — {APP_NAME}")
        self.setFixedWidth(400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(24, 20, 24, 20)

        # ── Logo + nom logiciel ──────────────────────────────────────────
        logo_label = QLabel()
        pixmap = QPixmap(get_logo_path())
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(56, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        name_label = QLabel(APP_NAME)
        name_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #2C5F8A;")
        layout.addWidget(name_label)

        sub_label = QLabel("Logiciel de gestion comptable")
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("color: #7F8C8D; font-size: 9pt; font-style: italic;")
        layout.addWidget(sub_label)

        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #95A5A6; font-size: 9pt;")
        layout.addWidget(version_label)

        # ── Développeur (hardcodé) ────────────────────────────────────────
        _separator(layout)
        layout.addWidget(_section_title("Développeur"))

        dev_lines = [
            _DEV["name"],
            _DEV["address"],
            _DEV["city"],
            f"Tél : {_DEV['phone']}",
            f"Email : {_DEV['email']}",
        ]
        dev_label = QLabel("\n".join(dev_lines))
        dev_label.setStyleSheet("color: #555; font-size: 9pt; line-height: 1.5;")
        dev_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(dev_label)

        # ── Entreprise (depuis company.json) ─────────────────────────────
        _separator(layout)
        layout.addWidget(_section_title("Entreprise"))

        company_lines = []
        primary = COMPANY.get("legal") or COMPANY.get("name", "")
        if primary:
            company_lines.append(primary)
        addr = COMPANY.get("address", "")
        city_line = " ".join(filter(None, [COMPANY.get("postal_code", ""), COMPANY.get("city", "")]))
        if addr:
            company_lines.append(addr)
        if city_line:
            company_lines.append(city_line)
        if COMPANY.get("phone"):
            company_lines.append(f"Tél : {COMPANY['phone']}")
        if COMPANY.get("email"):
            company_lines.append(f"Email : {COMPANY['email']}")
        if COMPANY.get("siret"):
            company_lines.append(f"SIRET : {COMPANY['siret']}")
        if COMPANY.get("tva_intra"):
            company_lines.append(f"TVA intra : {COMPANY['tva_intra']}")

        company_label = QLabel("\n".join(company_lines) if company_lines else "(non configurée)")
        company_label.setStyleSheet("color: #555; font-size: 9pt; line-height: 1.5;")
        company_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(company_label)

        # ── Bouton Fermer ─────────────────────────────────────────────────
        _separator(layout)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_fermer = QPushButton("Fermer")
        btn_fermer.setObjectName("quitterButton")
        btn_fermer.clicked.connect(self.accept)
        btn_layout.addWidget(btn_fermer)
        layout.addLayout(btn_layout)
