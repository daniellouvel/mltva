from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QHeaderView, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from database import DatabaseManager
from util import convert_month_to_number, PeriodeManager

MOIS_NOMS = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]


class SyntheseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Synthèse comptable")
        self.setMinimumSize(680, 480)
        self.setModal(True)

        self.db_manager = DatabaseManager()
        self.periode_manager = PeriodeManager()
        self.mois, self.annee = self.periode_manager.get_periode()

        layout = QVBoxLayout(self)

        titre = QLabel(f"Synthèse — {self.mois} {self.annee}")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        titre.setFont(font)
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_mensuel(), f"Mois — {self.mois} {self.annee}")
        self.tabs.addTab(self._build_annuel(), f"Année {self.annee}")
        layout.addWidget(self.tabs)

        fermer = QPushButton("Fermer")
        fermer.clicked.connect(self.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(fermer)
        layout.addLayout(btn_layout)

    def _get_mensuel_data(self, mois_num, annee):
        mois_str = f"{mois_num:02d}"
        annee_str = str(annee)

        dep = self.db_manager.fetch_all(
            "SELECT COALESCE(SUM(ttc),0), COALESCE(SUM(montant_tva),0) FROM depenses "
            "WHERE strftime('%m', date)=? AND strftime('%Y', date)=?",
            (mois_str, annee_str)
        )
        rec = self.db_manager.fetch_all(
            "SELECT COALESCE(SUM(montant),0), COALESCE(SUM(montant_tva),0) FROM recettes "
            "WHERE strftime('%m', date)=? AND strftime('%Y', date)=?",
            (mois_str, annee_str)
        )

        ttc_dep = float(dep[0][0]) if dep else 0.0
        tva_dep = float(dep[0][1]) if dep else 0.0
        ttc_rec = float(rec[0][0]) if rec else 0.0
        tva_rec = float(rec[0][1]) if rec else 0.0

        return ttc_dep, tva_dep, ttc_rec, tva_rec

    def _build_mensuel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        mois_num = convert_month_to_number(self.mois)
        ttc_dep, tva_dep, ttc_rec, tva_rec = self._get_mensuel_data(mois_num, self.annee)

        solde = ttc_rec - ttc_dep
        tva_reverser = tva_rec - tva_dep

        layout.addWidget(self._section("Dépenses", [
            ("Total TTC", ttc_dep),
            ("TVA déductible", tva_dep),
        ], couleur="#ffe0e0"))

        layout.addWidget(self._section("Recettes", [
            ("Total TTC", ttc_rec),
            ("TVA collectée", tva_rec),
        ], couleur="#e0ffe0"))

        layout.addWidget(self._section("Bilan", [
            ("Solde (Recettes − Dépenses)", solde),
            ("TVA à reverser (Collectée − Déductible)", tva_reverser),
        ], couleur="#e0e8ff", gras=True))

        layout.addStretch()
        return widget

    def _section(self, titre, lignes, couleur="#f5f5f5", gras=False):
        frame = QFrame()
        frame.setStyleSheet(f"background-color: {couleur}; border-radius: 6px; padding: 4px;")
        layout = QVBoxLayout(frame)

        label = QLabel(titre)
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)

        for nom, valeur in lignes:
            row = QHBoxLayout()
            l_nom = QLabel(nom)
            l_val = QLabel(f"{valeur:,.2f} €".replace(",", " "))
            if gras:
                font2 = QFont()
                font2.setBold(True)
                l_nom.setFont(font2)
                l_val.setFont(font2)
            couleur_val = "green" if valeur >= 0 else "red"
            l_val.setStyleSheet(f"color: {couleur_val};")
            l_val.setAlignment(Qt.AlignRight)
            row.addWidget(l_nom)
            row.addWidget(l_val)
            layout.addLayout(row)

        return frame

    def _build_annuel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Mois", "TTC Dépenses", "TVA Dép.", "TTC Recettes", "TVA Rec.", "Solde", "TVA à reverser"
        ])
        table.setRowCount(13)  # 12 mois + total
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for col in range(1, 7):
            table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

        total_ttc_dep = total_tva_dep = total_ttc_rec = total_tva_rec = 0.0

        for i, mois_nom in enumerate(MOIS_NOMS):
            ttc_dep, tva_dep, ttc_rec, tva_rec = self._get_mensuel_data(i + 1, self.annee)
            solde = ttc_rec - ttc_dep
            tva_reverser = tva_rec - tva_dep

            total_ttc_dep += ttc_dep
            total_tva_dep += tva_dep
            total_ttc_rec += ttc_rec
            total_tva_rec += tva_rec

            valeurs = [mois_nom, ttc_dep, tva_dep, ttc_rec, tva_rec, solde, tva_reverser]
            for col, val in enumerate(valeurs):
                if col == 0:
                    item = QTableWidgetItem(val)
                else:
                    item = QTableWidgetItem(f"{val:,.2f}".replace(",", " "))
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    if col in (5, 6):
                        item.setForeground(QColor("green") if val >= 0 else QColor("red"))
                table.setItem(i, col, item)

        # Ligne total
        total_solde = total_ttc_rec - total_ttc_dep
        total_tva_reverser = total_tva_rec - total_tva_dep
        totaux = ["TOTAL", total_ttc_dep, total_tva_dep, total_ttc_rec, total_tva_rec, total_solde, total_tva_reverser]
        font_bold = QFont()
        font_bold.setBold(True)
        for col, val in enumerate(totaux):
            if col == 0:
                item = QTableWidgetItem(val)
            else:
                item = QTableWidgetItem(f"{val:,.2f}".replace(",", " "))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if col in (5, 6):
                    item.setForeground(QColor("green") if val >= 0 else QColor("red"))
            item.setFont(font_bold)
            item.setBackground(QColor("#e0e8ff"))
            table.setItem(12, col, item)

        layout.addWidget(table)
        return widget
