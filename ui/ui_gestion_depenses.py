# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gestion_depenses.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCalendarWidget, QCheckBox,
    QComboBox, QDialog, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1114, 800)
        self.quitterButton = QPushButton(Dialog)
        self.quitterButton.setObjectName(u"quitterButton")
        self.quitterButton.setGeometry(QRect(1020, 750, 91, 41))
        self.tableWidget = QTableWidget(Dialog)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 310, 1101, 431))
        self.tableWidget.setMinimumSize(QSize(1101, 0))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.verticalHeader().setVisible(False)
        self.calendarWidget = QCalendarWidget(Dialog)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setEnabled(True)
        self.calendarWidget.setGeometry(QRect(250, 20, 256, 190))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(360, 20, 368, 32))
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.splitter.addWidget(self.label)
        self.moisLabel = QLabel(self.splitter)
        self.moisLabel.setObjectName(u"moisLabel")
        self.moisLabel.setStyleSheet(u"font: 18pt \"Segoe UI\";")
        self.splitter.addWidget(self.moisLabel)
        self.anneeLabel = QLabel(self.splitter)
        self.anneeLabel.setObjectName(u"anneeLabel")
        self.anneeLabel.setStyleSheet(u"font: 18pt \"Segoe UI\";")
        self.splitter.addWidget(self.anneeLabel)
        self.Saisie2em2ligne = QFrame(Dialog)
        self.Saisie2em2ligne.setObjectName(u"Saisie2em2ligne")
        self.Saisie2em2ligne.setGeometry(QRect(250, 110, 233, 150))
        self.gridLayout_2 = QGridLayout(self.Saisie2em2ligne)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelMontantTVA_2 = QLabel(self.Saisie2em2ligne)
        self.labelMontantTVA_2.setObjectName(u"labelMontantTVA_2")

        self.gridLayout_2.addWidget(self.labelMontantTVA_2, 2, 0, 1, 1)

        self.lineEditMontant_2 = QLineEdit(self.Saisie2em2ligne)
        self.lineEditMontant_2.setObjectName(u"lineEditMontant_2")

        self.gridLayout_2.addWidget(self.lineEditMontant_2, 0, 1, 1, 1)

        self.checkBoxValidation_2 = QCheckBox(self.Saisie2em2ligne)
        self.checkBoxValidation_2.setObjectName(u"checkBoxValidation_2")

        self.gridLayout_2.addWidget(self.checkBoxValidation_2, 4, 1, 1, 1)

        self.labelTTC_2 = QLabel(self.Saisie2em2ligne)
        self.labelTTC_2.setObjectName(u"labelTTC_2")

        self.gridLayout_2.addWidget(self.labelTTC_2, 0, 0, 1, 1)

        self.lineEditMontantTVA_2 = QLineEdit(self.Saisie2em2ligne)
        self.lineEditMontantTVA_2.setObjectName(u"lineEditMontantTVA_2")

        self.gridLayout_2.addWidget(self.lineEditMontantTVA_2, 2, 1, 1, 1)

        self.labelComentaire_2 = QLabel(self.Saisie2em2ligne)
        self.labelComentaire_2.setObjectName(u"labelComentaire_2")

        self.gridLayout_2.addWidget(self.labelComentaire_2, 3, 0, 1, 1)

        self.comboBoxTVA_2 = QComboBox(self.Saisie2em2ligne)
        self.comboBoxTVA_2.addItem("")
        self.comboBoxTVA_2.addItem("")
        self.comboBoxTVA_2.addItem("")
        self.comboBoxTVA_2.addItem("")
        self.comboBoxTVA_2.setObjectName(u"comboBoxTVA_2")

        self.gridLayout_2.addWidget(self.comboBoxTVA_2, 1, 1, 1, 1)

        self.labelTVA_2 = QLabel(self.Saisie2em2ligne)
        self.labelTVA_2.setObjectName(u"labelTVA_2")

        self.gridLayout_2.addWidget(self.labelTVA_2, 1, 0, 1, 1)

        self.lineEditComentaire_2 = QLineEdit(self.Saisie2em2ligne)
        self.lineEditComentaire_2.setObjectName(u"lineEditComentaire_2")

        self.gridLayout_2.addWidget(self.lineEditComentaire_2, 3, 1, 1, 1)

        self.layoutWidgetTotal = QWidget(Dialog)
        self.layoutWidgetTotal.setObjectName(u"layoutWidgetTotal")
        self.layoutWidgetTotal.setGeometry(QRect(10, 770, 432, 24))
        self.total = QGridLayout(self.layoutWidgetTotal)
        self.total.setObjectName(u"total")
        self.total.setContentsMargins(0, 0, 0, 0)
        self.labeltotalttc = QLabel(self.layoutWidgetTotal)
        self.labeltotalttc.setObjectName(u"labeltotalttc")

        self.total.addWidget(self.labeltotalttc, 0, 0, 1, 1)

        self.lineEdittotalttc = QLineEdit(self.layoutWidgetTotal)
        self.lineEdittotalttc.setObjectName(u"lineEdittotalttc")

        self.total.addWidget(self.lineEdittotalttc, 0, 1, 1, 1)

        self.labelmontanttva = QLabel(self.layoutWidgetTotal)
        self.labelmontanttva.setObjectName(u"labelmontanttva")

        self.total.addWidget(self.labelmontanttva, 0, 2, 1, 1)

        self.lineEditmontanttva = QLineEdit(self.layoutWidgetTotal)
        self.lineEditmontanttva.setObjectName(u"lineEditmontanttva")

        self.total.addWidget(self.lineEditmontanttva, 0, 3, 1, 1)

        self.layoutWidgetBoutons = QWidget(Dialog)
        self.layoutWidgetBoutons.setObjectName(u"layoutWidgetBoutons")
        self.layoutWidgetBoutons.setGeometry(QRect(20, 260, 411, 26))
        self.bouton = QGridLayout(self.layoutWidgetBoutons)
        self.bouton.setObjectName(u"bouton")
        self.bouton.setContentsMargins(0, 0, 0, 0)
        self.pushButtonEffacer = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonEffacer.setObjectName(u"pushButtonEffacer")

        self.bouton.addWidget(self.pushButtonEffacer, 0, 3, 1, 1)

        self.pushButtonModifier = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonModifier.setObjectName(u"pushButtonModifier")

        self.bouton.addWidget(self.pushButtonModifier, 0, 2, 1, 1)

        self.pushButtonValider = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonValider.setObjectName(u"pushButtonValider")

        self.bouton.addWidget(self.pushButtonValider, 0, 0, 1, 1)

        self.checkBox2emeLigne = QCheckBox(self.layoutWidgetBoutons)
        self.checkBox2emeLigne.setObjectName(u"checkBox2emeLigne")

        self.bouton.addWidget(self.checkBox2emeLigne, 0, 1, 1, 1)

        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 60, 216, 190))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelDate = QLabel(self.layoutWidget)
        self.labelDate.setObjectName(u"labelDate")

        self.gridLayout.addWidget(self.labelDate, 0, 0, 1, 1)

        self.lineEditDate = QLineEdit(self.layoutWidget)
        self.lineEditDate.setObjectName(u"lineEditDate")

        self.gridLayout.addWidget(self.lineEditDate, 0, 1, 1, 1)

        self.labelForniseur = QLabel(self.layoutWidget)
        self.labelForniseur.setObjectName(u"labelForniseur")

        self.gridLayout.addWidget(self.labelForniseur, 1, 0, 1, 1)

        self.comboBoxFournisseur = QComboBox(self.layoutWidget)
        self.comboBoxFournisseur.setObjectName(u"comboBoxFournisseur")

        self.gridLayout.addWidget(self.comboBoxFournisseur, 1, 1, 1, 1)

        self.labelTTC = QLabel(self.layoutWidget)
        self.labelTTC.setObjectName(u"labelTTC")

        self.gridLayout.addWidget(self.labelTTC, 2, 0, 1, 1)

        self.lineEditMontant = QLineEdit(self.layoutWidget)
        self.lineEditMontant.setObjectName(u"lineEditMontant")

        self.gridLayout.addWidget(self.lineEditMontant, 2, 1, 1, 1)

        self.labelTVA = QLabel(self.layoutWidget)
        self.labelTVA.setObjectName(u"labelTVA")

        self.gridLayout.addWidget(self.labelTVA, 3, 0, 1, 1)

        self.comboBoxTVA = QComboBox(self.layoutWidget)
        self.comboBoxTVA.setObjectName(u"comboBoxTVA")

        self.gridLayout.addWidget(self.comboBoxTVA, 3, 1, 1, 1)

        self.labelMontantTVA = QLabel(self.layoutWidget)
        self.labelMontantTVA.setObjectName(u"labelMontantTVA")

        self.gridLayout.addWidget(self.labelMontantTVA, 4, 0, 1, 1)

        self.lineEditMontantTVA = QLineEdit(self.layoutWidget)
        self.lineEditMontantTVA.setObjectName(u"lineEditMontantTVA")

        self.gridLayout.addWidget(self.lineEditMontantTVA, 4, 1, 1, 1)

        self.labelComentaire = QLabel(self.layoutWidget)
        self.labelComentaire.setObjectName(u"labelComentaire")

        self.gridLayout.addWidget(self.labelComentaire, 5, 0, 1, 1)

        self.lineEditComentaire = QLineEdit(self.layoutWidget)
        self.lineEditComentaire.setObjectName(u"lineEditComentaire")

        self.gridLayout.addWidget(self.lineEditComentaire, 5, 1, 1, 1)

        self.checkBoxValidation = QCheckBox(self.layoutWidget)
        self.checkBoxValidation.setObjectName(u"checkBoxValidation")

        self.gridLayout.addWidget(self.checkBoxValidation, 6, 1, 1, 1)

        self.pushButtonSuprimer = QPushButton(Dialog)
        self.pushButtonSuprimer.setObjectName(u"pushButtonSuprimer")
        self.pushButtonSuprimer.setGeometry(QRect(920, 750, 91, 41))
        self.layoutWidgetTotal.raise_()
        self.layoutWidgetBoutons.raise_()
        self.layoutWidget.raise_()
        self.splitter.raise_()
        self.quitterButton.raise_()
        self.tableWidget.raise_()
        self.Saisie2em2ligne.raise_()
        self.calendarWidget.raise_()
        self.pushButtonSuprimer.raise_()

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.quitterButton.setText(QCoreApplication.translate("Dialog", u"Quitter", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Rep\u00e8re", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Date", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Fournisseur", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"TTC", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Taux TVA", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Montant TVA", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Validation", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Commentaire", None));
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:700;\">Gestion Des D\u00e9penses</span></p></body></html>", None))
        self.moisLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:18pt;\">Mois</span></p></body></html>", None))
        self.anneeLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:18pt;\">Ann\u00e9e</span></p></body></html>", None))
        self.labelMontantTVA_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Montant TVA :</p></body></html>", None))
        self.checkBoxValidation_2.setText(QCoreApplication.translate("Dialog", u"Validation", None))
        self.labelTTC_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>TTC :</p></body></html>", None))
        self.labelComentaire_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Comentaire :</p></body></html>", None))
        self.comboBoxTVA_2.setItemText(0, QCoreApplication.translate("Dialog", u"0%", None))
        self.comboBoxTVA_2.setItemText(1, QCoreApplication.translate("Dialog", u"5.5%", None))
        self.comboBoxTVA_2.setItemText(2, QCoreApplication.translate("Dialog", u"10%", None))
        self.comboBoxTVA_2.setItemText(3, QCoreApplication.translate("Dialog", u"20%", None))

        self.labelTVA_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>TVA :</p></body></html>", None))
        self.labeltotalttc.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Total TTC</p></body></html>", None))
        self.labelmontanttva.setText(QCoreApplication.translate("Dialog", u"Total Montant TVA", None))
        self.pushButtonEffacer.setText(QCoreApplication.translate("Dialog", u"Effacer", None))
        self.pushButtonModifier.setText(QCoreApplication.translate("Dialog", u"Modifier", None))
        self.pushButtonValider.setText(QCoreApplication.translate("Dialog", u"Valider", None))
        self.checkBox2emeLigne.setText(QCoreApplication.translate("Dialog", u"2eme Ligne", None))
        self.labelDate.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Date :</p></body></html>", None))
        self.labelForniseur.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Fournisseur :</p></body></html>", None))
        self.labelTTC.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>TTC :</p></body></html>", None))
        self.labelTVA.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>TVA :</p></body></html>", None))
        self.labelMontantTVA.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Montant TVA :</p></body></html>", None))
        self.labelComentaire.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Comentaire :</p></body></html>", None))
        self.checkBoxValidation.setText(QCoreApplication.translate("Dialog", u"Validation", None))
        self.pushButtonSuprimer.setText(QCoreApplication.translate("Dialog", u"Suprimer", None))
    # retranslateUi

