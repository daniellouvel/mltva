# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSplitter,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionContacts = QAction(MainWindow)
        self.actionContacts.setObjectName(u"actionContacts")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(500, 30, 261, 121))
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.splitter.addWidget(self.label)
        self.labellogo = QLabel(self.centralwidget)
        self.labellogo.setObjectName(u"labellogo")
        self.labellogo.setGeometry(QRect(10, 10, 427, 163))
        self.labellogo.setPixmap(QPixmap(u"../data/Logo.jpg"))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(280, 220, 211, 59))
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"}\n"
"")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.moisComboBox = QComboBox(self.groupBox_2)
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.addItem("")
        self.moisComboBox.setObjectName(u"moisComboBox")

        self.horizontalLayout.addWidget(self.moisComboBox)

        self.anneeLineEdit = QLineEdit(self.groupBox_2)
        self.anneeLineEdit.setObjectName(u"anneeLineEdit")

        self.horizontalLayout.addWidget(self.anneeLineEdit)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.groupBoxpreiode = QGroupBox(self.centralwidget)
        self.groupBoxpreiode.setObjectName(u"groupBoxpreiode")
        self.groupBoxpreiode.setGeometry(QRect(280, 320, 191, 211))
        self.groupBoxpreiode.setStyleSheet(u"QGroupBox {\n"
"    border: none;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.groupBoxpreiode)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.depensesButton = QPushButton(self.groupBoxpreiode)
        self.depensesButton.setObjectName(u"depensesButton")

        self.verticalLayout.addWidget(self.depensesButton)

        self.recettesButton = QPushButton(self.groupBoxpreiode)
        self.recettesButton.setObjectName(u"recettesButton")

        self.verticalLayout.addWidget(self.recettesButton)

        self.pushButton_export_pdf = QPushButton(self.groupBoxpreiode)
        self.pushButton_export_pdf.setObjectName(u"pushButton_export_pdf")

        self.verticalLayout.addWidget(self.pushButton_export_pdf)

        self.pusharegeler = QPushButton(self.groupBoxpreiode)
        self.pusharegeler.setObjectName(u"pusharegeler")

        self.verticalLayout.addWidget(self.pusharegeler)

        self.quitterButton = QPushButton(self.groupBoxpreiode)
        self.quitterButton.setObjectName(u"quitterButton")

        self.verticalLayout.addWidget(self.quitterButton)

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 2, 2))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuConfig = QMenu(self.menubar)
        self.menuConfig.setObjectName(u"menuConfig")
        self.menuAide = QMenu(self.menubar)
        self.menuAide.setObjectName(u"menuAide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.menuConfig.addSeparator()
        self.menuConfig.addAction(self.actionContacts)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionContacts.setText(QCoreApplication.translate("MainWindow", u"Contacts", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:48pt; font-style:italic;\">MLTVA</span></p></body></html>", None))
        self.labellogo.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"P\u00ebriode", None))
        self.moisComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Janvier", None))
        self.moisComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"F\u00e9vrier", None))
        self.moisComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Mars", None))
        self.moisComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Avril", None))
        self.moisComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Mai", None))
        self.moisComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Juin", None))
        self.moisComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"Juillet", None))
        self.moisComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"Ao\u00fbt", None))
        self.moisComboBox.setItemText(8, QCoreApplication.translate("MainWindow", u"Septembre", None))
        self.moisComboBox.setItemText(9, QCoreApplication.translate("MainWindow", u"Octobre", None))
        self.moisComboBox.setItemText(10, QCoreApplication.translate("MainWindow", u"Novembre", None))
        self.moisComboBox.setItemText(11, QCoreApplication.translate("MainWindow", u"D\u00e9cembre", None))

        self.groupBoxpreiode.setTitle("")
        self.depensesButton.setText(QCoreApplication.translate("MainWindow", u"D\u00e9pences", None))
        self.recettesButton.setText(QCoreApplication.translate("MainWindow", u"Recettes", None))
        self.pushButton_export_pdf.setText(QCoreApplication.translate("MainWindow", u"Export PDF", None))
#if QT_CONFIG(tooltip)
        self.pusharegeler.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">founiseur a</p><p align=\"center\">regler</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.pusharegeler.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Fonineur a</p><p align=\"center\">Regler</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.pusharegeler.setText(QCoreApplication.translate("MainWindow", u"A regler", None))
        self.quitterButton.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
        self.menuConfig.setTitle(QCoreApplication.translate("MainWindow", u"Config", None))
        self.menuAide.setTitle(QCoreApplication.translate("MainWindow", u"Aide", None))
    # retranslateUi

