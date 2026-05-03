# -*- coding: utf-8 -*-
# Réécrit avec layouts dynamiques (QVBoxLayout/QHBoxLayout/QGridLayout)
# pour remplacer le positionnement absolu généré par Qt Designer.

from PySide6.QtCore import QMetaObject
from PySide6.QtWidgets import (
    QAbstractItemView, QCalendarWidget, QCheckBox, QComboBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
)
from PySide6.QtGui import QFont


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(1114, 800)
        Dialog.setWindowTitle("Gestion des Recettes")

        main_layout = QVBoxLayout(Dialog)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # --- En-tête : titre + mois + année ---
        header = QHBoxLayout()
        self.label = QLabel()
        self.label.setText("<html><body><p align='center'><span style='font-size:18pt; font-weight:700;'>Gestion Des Recettes : </span></p></body></html>")
        self.moisLabel = QLabel()
        self.moisLabel.setObjectName("moisLabel")
        self.moisLabel.setStyleSheet("font: 18pt 'Segoe UI';")
        self.anneeLabel = QLabel()
        self.anneeLabel.setObjectName("anneeLabel")
        self.anneeLabel.setStyleSheet("font: 18pt 'Segoe UI';")
        header.addStretch()
        header.addWidget(self.label)
        header.addWidget(self.moisLabel)
        header.addWidget(self.anneeLabel)
        header.addStretch()
        main_layout.addLayout(header)

        # --- Zone saisie : formulaire + calendrier ---
        middle = QHBoxLayout()

        form_widget = QWidget()
        self.gridLayout = QGridLayout(form_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.labelDate = QLabel("Date :")
        self.lineEditDate = QLineEdit()
        self.lineEditDate.setObjectName("lineEditDate")
        self.gridLayout.addWidget(self.labelDate, 0, 0)
        self.gridLayout.addWidget(self.lineEditDate, 0, 1)

        self.labelClient = QLabel("Client :")
        self.comboBoxFournisseur = QComboBox()
        self.comboBoxFournisseur.setObjectName("comboBoxFournisseur")
        self.gridLayout.addWidget(self.labelClient, 1, 0)
        self.gridLayout.addWidget(self.comboBoxFournisseur, 1, 1)

        self.label_2 = QLabel("Paiement :")
        self.comboBoxPaiement = QComboBox()
        self.comboBoxPaiement.setObjectName("comboBoxPaiement")
        self.gridLayout.addWidget(self.label_2, 2, 0)
        self.gridLayout.addWidget(self.comboBoxPaiement, 2, 1)

        self.label_3 = QLabel("N°facture :")
        self.lineEditnfacture = QLineEdit()
        self.lineEditnfacture.setObjectName("lineEditnfacture")
        self.gridLayout.addWidget(self.label_3, 3, 0)
        self.gridLayout.addWidget(self.lineEditnfacture, 3, 1)

        self.labelTTC = QLabel("Montant :")
        self.lineEditMontant = QLineEdit()
        self.lineEditMontant.setObjectName("lineEditMontant")
        self.gridLayout.addWidget(self.labelTTC, 4, 0)
        self.gridLayout.addWidget(self.lineEditMontant, 4, 1)

        self.labelTVA = QLabel("TVA :")
        self.comboBoxTVA = QComboBox()
        self.comboBoxTVA.setObjectName("comboBoxTVA")
        self.gridLayout.addWidget(self.labelTVA, 5, 0)
        self.gridLayout.addWidget(self.comboBoxTVA, 5, 1)

        self.labelMontantTVA = QLabel("Montant TVA :")
        self.lineEditMontantTVA = QLineEdit()
        self.lineEditMontantTVA.setObjectName("lineEditMontantTVA")
        self.gridLayout.addWidget(self.labelMontantTVA, 6, 0)
        self.gridLayout.addWidget(self.lineEditMontantTVA, 6, 1)

        self.labelCommentaire = QLabel("Commentaire :")
        self.lineEditCommentaire = QLineEdit()
        self.lineEditCommentaire.setObjectName("lineEditCommentaire")
        self.gridLayout.addWidget(self.labelCommentaire, 7, 0)
        self.gridLayout.addWidget(self.lineEditCommentaire, 7, 1)

        self.checkBox2emeLigne = QCheckBox("2ème ligne (TVA différente)")
        self.checkBox2emeLigne.setObjectName("checkBox2emeLigne")
        self.gridLayout.addWidget(self.checkBox2emeLigne, 8, 0, 1, 2)

        self.labelMontant2 = QLabel("Montant (2ème) :")
        self.lineEditMontant2 = QLineEdit()
        self.lineEditMontant2.setObjectName("lineEditMontant2")
        self.gridLayout.addWidget(self.labelMontant2, 9, 0)
        self.gridLayout.addWidget(self.lineEditMontant2, 9, 1)

        self.labelTVA2 = QLabel("TVA (2ème) :")
        self.comboBoxTVA2 = QComboBox()
        self.comboBoxTVA2.setObjectName("comboBoxTVA2")
        self.gridLayout.addWidget(self.labelTVA2, 10, 0)
        self.gridLayout.addWidget(self.comboBoxTVA2, 10, 1)

        self.labelMontantTVA2 = QLabel("Montant TVA (2ème) :")
        self.lineEditMontantTVA2 = QLineEdit()
        self.lineEditMontantTVA2.setObjectName("lineEditMontantTVA2")
        self.gridLayout.addWidget(self.labelMontantTVA2, 11, 0)
        self.gridLayout.addWidget(self.lineEditMontantTVA2, 11, 1)

        for w in [self.labelMontant2, self.lineEditMontant2, self.labelTVA2,
                  self.comboBoxTVA2, self.labelMontantTVA2, self.lineEditMontantTVA2]:
            w.setVisible(False)

        # Calendrier (caché par défaut)
        self.calendarWidget = QCalendarWidget()
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setVisible(False)

        left_layout = QVBoxLayout()
        left_layout.addWidget(form_widget)
        left_layout.addWidget(self.calendarWidget)
        left_layout.addStretch()

        middle.addLayout(left_layout)
        middle.addStretch()
        main_layout.addLayout(middle)

        # --- Boutons d'action ---
        btn_layout = QHBoxLayout()
        self.pushButtonValider = QPushButton("Valider")
        self.pushButtonValider.setObjectName("pushButtonValider")
        self.pushButtonModifier = QPushButton("Modifier")
        self.pushButtonModifier.setObjectName("pushButtonModifier")
        self.pushButtonEffacer = QPushButton("Effacer")
        self.pushButtonEffacer.setObjectName("pushButtonEffacer")
        self.push_calculettettc = QPushButton("Calculette TTC")
        self.push_calculettettc.setObjectName("push_calculettettc")
        btn_layout.addWidget(self.pushButtonValider)
        btn_layout.addWidget(self.pushButtonModifier)
        btn_layout.addWidget(self.pushButtonEffacer)
        btn_layout.addWidget(self.push_calculettettc)
        btn_layout.addStretch()
        label_f1 = QLabel("F1 : Aide")
        label_f1.setStyleSheet("color: #95A5A6; font-style: italic;")
        btn_layout.addWidget(label_f1)
        main_layout.addLayout(btn_layout)

        # --- Tableau principal (s'étire) ---
        self.tableWidget = QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        headers = ["Repère", "Date", "Client", "Paiement", "N°Facture", "Montant", "Taux TVA", "Montant TVA", "Commentaire"]
        for i, h in enumerate(headers):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(h))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.verticalHeader().setVisible(False)
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tableWidget.setSizePolicy(sp)
        main_layout.addWidget(self.tableWidget, stretch=1)

        # --- Pied de page : totaux + boutons ---
        footer = QHBoxLayout()
        self.labeltotalttc = QLabel("Montant Total")
        self.labeltotalttc.setObjectName("labeltotalttc")
        self.lineEditMontantTotal = QLineEdit()
        self.lineEditMontantTotal.setObjectName("lineEditMontantTotal")
        self.lineEditMontantTotal.setMaximumWidth(120)
        self.labelmontanttva = QLabel("Total Montant TVA")
        self.labelmontanttva.setObjectName("labelmontanttva")
        self.lineEditTotalMontantTVA = QLineEdit()
        self.lineEditTotalMontantTVA.setObjectName("lineEditTotalMontantTVA")
        self.lineEditTotalMontantTVA.setMaximumWidth(120)
        self.pushButtonSupprimer = QPushButton("Supprimer")
        self.pushButtonSupprimer.setObjectName("pushButtonSupprimer")
        self.quitterButton = QPushButton("Quitter")
        self.quitterButton.setObjectName("quitterButton")
        footer.addWidget(self.labeltotalttc)
        footer.addWidget(self.lineEditMontantTotal)
        footer.addWidget(self.labelmontanttva)
        footer.addWidget(self.lineEditTotalMontantTVA)
        footer.addStretch()
        footer.addWidget(self.pushButtonSupprimer)
        footer.addWidget(self.quitterButton)
        main_layout.addLayout(footer)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass
