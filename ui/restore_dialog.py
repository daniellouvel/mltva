import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from utils.backup import backup_database
from company_config import get_backup_dir, get_db_path


class RestoreDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Restaurer une sauvegarde")
        self.setMinimumSize(500, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Sélectionnez la sauvegarde à restaurer :"))

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Fichier", "Type", "Date"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.restore_button = QPushButton("Restaurer")
        self.restore_button.setEnabled(False)
        cancel_button = QPushButton("Annuler")
        button_layout.addWidget(self.restore_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.restore_button.clicked.connect(self.restore)
        cancel_button.clicked.connect(self.reject)
        self.table.selectionModel().selectionChanged.connect(
            lambda: self.restore_button.setEnabled(len(self.table.selectedItems()) > 0)
        )

        self._load_backups()

    def _load_backups(self):
        backup_dir = get_backup_dir()
        if not os.path.exists(backup_dir):
            return

        backups = []
        for f in os.listdir(backup_dir):
            if not f.startswith("mlbdd_") or not f.endswith(".db"):
                continue
            name = f[6:-3]  # strip "mlbdd_" and ".db"
            if len(name) == 10:   # 2026-05-02
                btype = "Journalier"
                try:
                    date = datetime.strptime(name, "%Y-%m-%d").strftime("%d/%m/%Y")
                except ValueError:
                    continue
            elif len(name) == 7:  # 2026-05
                btype = "Mensuel"
                try:
                    date = datetime.strptime(name, "%Y-%m").strftime("%m/%Y")
                except ValueError:
                    continue
            elif len(name) == 4:  # 2026
                btype = "Annuel"
                date = name
            else:
                continue
            backups.append((f, btype, date, name))

        backups.sort(key=lambda x: x[3], reverse=True)

        self.table.setRowCount(len(backups))
        for row, (filename, btype, date, _) in enumerate(backups):
            self.table.setItem(row, 0, QTableWidgetItem(filename))
            self.table.setItem(row, 1, QTableWidgetItem(btype))
            self.table.setItem(row, 2, QTableWidgetItem(date))
            self._center(row, 1)
            self._center(row, 2)

    def _center(self, row, col):
        item = self.table.item(row, col)
        if item:
            item.setTextAlignment(Qt.AlignCenter)

    def restore(self):
        row = self.table.currentRow()
        if row < 0:
            return

        filename = self.table.item(row, 0).text()
        source = os.path.join(get_backup_dir(), filename)

        reply = QMessageBox.question(
            self,
            "Confirmer la restauration",
            f"Restaurer la sauvegarde :\n{filename}\n\n"
            "La base de données actuelle sera sauvegardée avant la restauration.\n\n"
            "Continuer ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        try:
            # Sauvegarde de sécurité avant restauration
            backup_database()

            # Restauration
            shutil.copy2(source, get_db_path())

            QMessageBox.information(
                self,
                "Restauration réussie",
                f"La sauvegarde a été restaurée avec succès.\n\n"
                "Veuillez redémarrer l'application pour prendre en compte les données restaurées."
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la restauration :\n{str(e)}")
