# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gestion_Recettes.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCalendarWidget, QComboBox,
    QDialog, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSplitter,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1114, 798)
        self.quitterButton = QPushButton(Dialog)
        self.quitterButton.setObjectName(u"quitterButton")
        self.quitterButton.setGeometry(QRect(1020, 740, 91, 41))
        self.tableWidget = QTableWidget(Dialog)
        if (self.tableWidget.columnCount() < 9):
            self.tableWidget.setColumnCount(9)
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
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 330, 1101, 401))
        self.tableWidget.setMinimumSize(QSize(1101, 0))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.tableWidget.verticalHeader().setVisible(False)
        self.calendarWidget = QCalendarWidget(Dialog)
        self.calendarWidget.setObjectName(u"calendarWidget")
        self.calendarWidget.setEnabled(True)
        self.calendarWidget.setGeometry(QRect(260, 50, 256, 190))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(197, 10, 511, 32))
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
        self.layoutWidgetBoutons = QWidget(Dialog)
        self.layoutWidgetBoutons.setObjectName(u"layoutWidgetBoutons")
        self.layoutWidgetBoutons.setGeometry(QRect(10, 280, 411, 26))
        self.bouton = QGridLayout(self.layoutWidgetBoutons)
        self.bouton.setObjectName(u"bouton")
        self.bouton.setContentsMargins(0, 0, 0, 0)
        self.pushButtonEffacer = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonEffacer.setObjectName(u"pushButtonEffacer")

        self.bouton.addWidget(self.pushButtonEffacer, 0, 2, 1, 1)

        self.pushButtonModifier = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonModifier.setObjectName(u"pushButtonModifier")

        self.bouton.addWidget(self.pushButtonModifier, 0, 1, 1, 1)

        self.pushButtonValider = QPushButton(self.layoutWidgetBoutons)
        self.pushButtonValider.setObjectName(u"pushButtonValider")

        self.bouton.addWidget(self.pushButtonValider, 0, 0, 1, 1)

        self.push_calculettettc = QPushButton(self.layoutWidgetBoutons)
        self.push_calculettettc.setObjectName(u"push_calculettettc")

        self.bouton.addWidget(self.push_calculettettc, 0, 3, 1, 1)

        self.pushButtonSuprimer = QPushButton(Dialog)
        self.pushButtonSuprimer.setObjectName(u"pushButtonSuprimer")
        self.pushButtonSuprimer.setGeometry(QRect(920, 740, 91, 41))
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 50, 216, 220))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.labelTVA = QLabel(self.layoutWidget)
        self.labelTVA.setObjectName(u"labelTVA")

        self.gridLayout.addWidget(self.labelTVA, 5, 0, 1, 1)

        self.lineEditMontantTVA = QLineEdit(self.layoutWidget)
        self.lineEditMontantTVA.setObjectName(u"lineEditMontantTVA")

        self.gridLayout.addWidget(self.lineEditMontantTVA, 6, 1, 1, 1)

        self.lineEditMontant = QLineEdit(self.layoutWidget)
        self.lineEditMontant.setObjectName(u"lineEditMontant")

        self.gridLayout.addWidget(self.lineEditMontant, 4, 1, 1, 1)

        self.labelForniseur = QLabel(self.layoutWidget)
        self.labelForniseur.setObjectName(u"labelForniseur")

        self.gridLayout.addWidget(self.labelForniseur, 1, 0, 1, 1)

        self.labelMontantTVA = QLabel(self.layoutWidget)
        self.labelMontantTVA.setObjectName(u"labelMontantTVA")

        self.gridLayout.addWidget(self.labelMontantTVA, 6, 0, 1, 1)

        self.lineEditnfacture = QLineEdit(self.layoutWidget)
        self.lineEditnfacture.setObjectName(u"lineEditnfacture")

        self.gridLayout.addWidget(self.lineEditnfacture, 3, 1, 1, 1)

        self.lineEditDate = QLineEdit(self.layoutWidget)
        self.lineEditDate.setObjectName(u"lineEditDate")

        self.gridLayout.addWidget(self.lineEditDate, 0, 1, 1, 1)

        self.comboBoxpayment = QComboBox(self.layoutWidget)
        self.comboBoxpayment.setObjectName(u"comboBoxpayment")

        self.gridLayout.addWidget(self.comboBoxpayment, 2, 1, 1, 1)

        self.labelTTC = QLabel(self.layoutWidget)
        self.labelTTC.setObjectName(u"labelTTC")

        self.gridLayout.addWidget(self.labelTTC, 4, 0, 1, 1)

        self.lineEditComentaire = QLineEdit(self.layoutWidget)
        self.lineEditComentaire.setObjectName(u"lineEditComentaire")

        self.gridLayout.addWidget(self.lineEditComentaire, 7, 1, 1, 1)

        self.comboBoxTVA = QComboBox(self.layoutWidget)
        self.comboBoxTVA.setObjectName(u"comboBoxTVA")

        self.gridLayout.addWidget(self.comboBoxTVA, 5, 1, 1, 1)

        self.labelComentaire = QLabel(self.layoutWidget)
        self.labelComentaire.setObjectName(u"labelComentaire")

        self.gridLayout.addWidget(self.labelComentaire, 7, 0, 1, 1)

        self.comboBoxFournisseur = QComboBox(self.layoutWidget)
        self.comboBoxFournisseur.setObjectName(u"comboBoxFournisseur")

        self.gridLayout.addWidget(self.comboBoxFournisseur, 1, 1, 1, 1)

        self.labelDate = QLabel(self.layoutWidget)
        self.labelDate.setObjectName(u"labelDate")

        self.gridLayout.addWidget(self.labelDate, 0, 0, 1, 1)

        self.lineEdittotalmontanttva = QLineEdit(Dialog)
        self.lineEdittotalmontanttva.setObjectName(u"lineEdittotalmontanttva")
        self.lineEdittotalmontanttva.setGeometry(QRect(337, 762, 132, 21))
        self.labelmontanttva = QLabel(Dialog)
        self.labelmontanttva.setObjectName(u"labelmontanttva")
        self.labelmontanttva.setGeometry(QRect(232, 762, 99, 16))
        self.labeltotalttc = QLabel(Dialog)
        self.labeltotalttc.setObjectName(u"labeltotalttc")
        self.labeltotalttc.setGeometry(QRect(13, 762, 75, 16))
        self.lineEdimontanttotal = QLineEdit(Dialog)
        self.lineEdimontanttotal.setObjectName(u"lineEdimontanttotal")
        self.lineEdimontanttotal.setGeometry(QRect(94, 762, 132, 21))
        self.pushButtonSuprimer.raise_()
        self.layoutWidget.raise_()
        self.lineEdittotalmontanttva.raise_()
        self.labelmontanttva.raise_()
        self.labeltotalttc.raise_()
        self.lineEdimontanttotal.raise_()
        self.layoutWidgetBoutons.raise_()
        self.splitter.raise_()
        self.quitterButton.raise_()
        self.tableWidget.raise_()
        self.calendarWidget.raise_()

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
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Paiement", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"N\u00b0facture", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Montant", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Taux TVA", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"Montant TVA", None));
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"Commentaire", None));
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:700;\">Gestion Des Recettes : </span></p></body></html>", None))
        self.moisLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:18pt;\">Mois</span></p></body></html>", None))
        self.anneeLabel.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:18pt;\">Ann\u00e9e</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.pushButtonEffacer.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButtonEffacer.setText(QCoreApplication.translate("Dialog", u"Effacer", None))
        self.pushButtonModifier.setText(QCoreApplication.translate("Dialog", u"Modifier", None))
        self.pushButtonValider.setText(QCoreApplication.translate("Dialog", u"Valider", None))
        self.push_calculettettc.setText(QCoreApplication.translate("Dialog", u"Calculette TTC", None))
        self.pushButtonSuprimer.setText(QCoreApplication.translate("Dialog", u"Supprimer", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"N\u00b0facture", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Paiement", None))
        self.labelTVA.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>TVA :</p></body></html>", None))
        self.labelForniseur.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Client</p></body></html>", None))
        self.labelMontantTVA.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Montant TVA :</p></body></html>", None))
        self.labelTTC.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Montant</p></body></html>", None))
        self.labelComentaire.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Comentaire :</p></body></html>", None))
        self.labelDate.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Date :</p></body></html>", None))
        self.labelmontanttva.setText(QCoreApplication.translate("Dialog", u"Total Montant TVA", None))
        self.labeltotalttc.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Montant Total</p></body></html>", None))
    # retranslateUi

