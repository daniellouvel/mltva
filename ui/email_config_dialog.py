from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QSpinBox, QPushButton, QHBoxLayout, QMessageBox, QGroupBox
)
from scan_email import load_email_config, save_email_config, test_connection


class EmailConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration email — Import factures")
        self.setMinimumWidth(480)
        self.setModal(True)
        self.config = load_email_config()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "Pour Gmail : activez l'accès IMAP dans les paramètres Gmail,\n"
            "puis créez un «Mot de passe d'application» dans votre compte Google\n"
            "(Sécurité → Validation en 2 étapes → Mots de passe des applications)."
        )
        info.setStyleSheet(
            "background:#FEF9E7; border:1px solid #F0B27A; "
            "padding:8px; border-radius:4px;"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        group = QGroupBox("Serveur IMAP")
        grid = QGridLayout(group)

        self.edit_server = QLineEdit(self.config.get("server", "imap.gmail.com"))
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1, 65535)
        self.spin_port.setValue(int(self.config.get("port", 993)))
        self.edit_email = QLineEdit(self.config.get("email", ""))
        self.edit_password = QLineEdit(self.config.get("password", ""))
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_dossier = QLineEdit(self.config.get("dossier", "INBOX"))
        self.spin_jours = QSpinBox()
        self.spin_jours.setRange(1, 365)
        self.spin_jours.setValue(int(self.config.get("jours", 30)))
        self.spin_jours.setSuffix(" jours")

        grid.addWidget(QLabel("Serveur IMAP :"), 0, 0)
        grid.addWidget(self.edit_server, 0, 1)
        grid.addWidget(QLabel("Port SSL :"), 1, 0)
        grid.addWidget(self.spin_port, 1, 1)
        grid.addWidget(QLabel("Adresse email :"), 2, 0)
        grid.addWidget(self.edit_email, 2, 1)
        grid.addWidget(QLabel("Mot de passe :"), 3, 0)
        grid.addWidget(self.edit_password, 3, 1)
        grid.addWidget(QLabel("Dossier :"), 4, 0)
        grid.addWidget(self.edit_dossier, 4, 1)
        grid.addWidget(QLabel("Importer les emails des :"), 5, 0)
        grid.addWidget(self.spin_jours, 5, 1)

        layout.addWidget(group)

        btn_layout = QHBoxLayout()
        btn_test = QPushButton("Tester la connexion")
        btn_test.setObjectName("pushButtonModifier")
        btn_ok = QPushButton("Enregistrer")
        btn_ok.setObjectName("pushButtonValider")
        btn_annuler = QPushButton("Annuler")
        btn_layout.addWidget(btn_test)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_annuler)
        layout.addLayout(btn_layout)

        btn_test.clicked.connect(self._test_connection)
        btn_ok.clicked.connect(self._save_and_accept)
        btn_annuler.clicked.connect(self.reject)

    def _get_config(self):
        return {
            "server": self.edit_server.text().strip(),
            "port": self.spin_port.value(),
            "email": self.edit_email.text().strip(),
            "password": self.edit_password.text(),
            "dossier": self.edit_dossier.text().strip() or "INBOX",
            "jours": self.spin_jours.value(),
        }

    def _test_connection(self):
        cfg = self._get_config()
        if not cfg["email"] or not cfg["password"]:
            QMessageBox.warning(self, "Champs manquants",
                                "Veuillez saisir l'adresse email et le mot de passe.")
            return
        ok, msg = test_connection(cfg["server"], cfg["port"], cfg["email"], cfg["password"])
        if ok:
            QMessageBox.information(self, "Connexion réussie",
                                    "Connexion IMAP établie avec succès.")
        else:
            QMessageBox.critical(self, "Échec de connexion",
                                 f"Impossible de se connecter :\n\n{msg}")

    def _save_and_accept(self):
        save_email_config(self._get_config())
        self.accept()
