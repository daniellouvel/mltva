from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

from company_config import COMPANY, get_logo_path
from version import APP_VERSION


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"À propos — {COMPANY['name']}")
        self.setFixedSize(380, 320)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(get_logo_path())
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToHeight(64, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Nom de l'application
        name_label = QLabel(COMPANY["name"])
        font = QFont("Segoe UI", 18, QFont.Bold)
        font.setItalic(True)
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #2C5F8A;")
        layout.addWidget(name_label)

        # Version
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #7F8C8D; font-size: 10pt;")
        layout.addWidget(version_label)

        # Informations légales
        legal_label = QLabel(COMPANY.get("legal", COMPANY["name"]))
        legal_label.setAlignment(Qt.AlignCenter)
        legal_label.setStyleSheet("color: #555; font-size: 9pt;")
        layout.addWidget(legal_label)

        # Coordonnées entreprise
        coord_lines = []
        addr = COMPANY.get("address", "")
        city_line = " ".join(filter(None, [COMPANY.get("postal_code", ""), COMPANY.get("city", "")]))
        if addr:
            coord_lines.append(addr)
        if city_line:
            coord_lines.append(city_line)
        if COMPANY.get("phone"):
            coord_lines.append(f"Tél : {COMPANY['phone']}")
        if COMPANY.get("email"):
            coord_lines.append(f"Email : {COMPANY['email']}")
        if COMPANY.get("siret"):
            coord_lines.append(f"SIRET : {COMPANY['siret']}")
        if COMPANY.get("tva_intra"):
            coord_lines.append(f"TVA intra : {COMPANY['tva_intra']}")
        if coord_lines:
            coord_label = QLabel("\n".join(coord_lines))
            coord_label.setAlignment(Qt.AlignCenter)
            coord_label.setStyleSheet("color: #7F8C8D; font-size: 8pt;")
            layout.addWidget(coord_label)

        layout.addStretch()

        # Bouton Fermer
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_fermer = QPushButton("Fermer")
        btn_fermer.setObjectName("quitterButton")
        btn_fermer.clicked.connect(self.accept)
        btn_layout.addWidget(btn_fermer)
        layout.addLayout(btn_layout)
