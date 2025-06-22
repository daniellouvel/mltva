# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'contacts_manager.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_ContactsManager(object):
    def setupUi(self, ContactsManager):
        if not ContactsManager.objectName():
            ContactsManager.setObjectName(u"ContactsManager")
        ContactsManager.resize(664, 636)
        self.centralwidget = QWidget(ContactsManager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.contacts_table = QTableWidget(self.centralwidget)
        if (self.contacts_table.columnCount() < 4):
            self.contacts_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.contacts_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.contacts_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.contacts_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.contacts_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.contacts_table.setObjectName(u"contacts_table")
        self.contacts_table.setGeometry(QRect(0, 180, 651, 381))
        self.contacts_table.setAlternatingRowColors(True)
        self.contacts_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.contacts_table.setRowCount(0)
        self.contacts_table.setColumnCount(4)
        self.pushButton_quitter = QPushButton(self.centralwidget)
        self.pushButton_quitter.setObjectName(u"pushButton_quitter")
        self.pushButton_quitter.setGeometry(QRect(560, 570, 91, 41))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 130, 311, 41))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.edit_button = QPushButton(self.gridLayoutWidget)
        self.edit_button.setObjectName(u"edit_button")

        self.gridLayout.addWidget(self.edit_button, 0, 1, 1, 1)

        self.add_button = QPushButton(self.gridLayoutWidget)
        self.add_button.setObjectName(u"add_button")

        self.gridLayout.addWidget(self.add_button, 0, 0, 1, 1)

        self.delete_button = QPushButton(self.gridLayoutWidget)
        self.delete_button.setObjectName(u"delete_button")

        self.gridLayout.addWidget(self.delete_button, 0, 2, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 271, 121))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.name_input = QLineEdit(self.gridLayoutWidget_2)
        self.name_input.setObjectName(u"name_input")

        self.gridLayout_2.addWidget(self.name_input, 0, 0, 1, 1)

        self.prenom_input = QLineEdit(self.gridLayoutWidget_2)
        self.prenom_input.setObjectName(u"prenom_input")

        self.gridLayout_2.addWidget(self.prenom_input, 1, 0, 1, 1)

        self.telephone_input = QLineEdit(self.gridLayoutWidget_2)
        self.telephone_input.setObjectName(u"telephone_input")

        self.gridLayout_2.addWidget(self.telephone_input, 2, 0, 1, 1)

        self.email_input = QLineEdit(self.gridLayoutWidget_2)
        self.email_input.setObjectName(u"email_input")

        self.gridLayout_2.addWidget(self.email_input, 3, 0, 1, 1)

        ContactsManager.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ContactsManager)
        self.statusbar.setObjectName(u"statusbar")
        ContactsManager.setStatusBar(self.statusbar)

        self.retranslateUi(ContactsManager)

        QMetaObject.connectSlotsByName(ContactsManager)
    # setupUi

    def retranslateUi(self, ContactsManager):
        ContactsManager.setWindowTitle(QCoreApplication.translate("ContactsManager", u"Gestion des Contacts", None))
        ___qtablewidgetitem = self.contacts_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ContactsManager", u"Nom", None));
        ___qtablewidgetitem1 = self.contacts_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ContactsManager", u"Pr\u00e9nom", None));
        ___qtablewidgetitem2 = self.contacts_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ContactsManager", u"T\u00e9l\u00e9phone", None));
        ___qtablewidgetitem3 = self.contacts_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ContactsManager", u"Email", None));
        self.contacts_table.setProperty(u"horizontalHeaderLabels", [])
        self.pushButton_quitter.setText(QCoreApplication.translate("ContactsManager", u"Quitter", None))
        self.edit_button.setText(QCoreApplication.translate("ContactsManager", u"Modifier", None))
        self.add_button.setText(QCoreApplication.translate("ContactsManager", u"Ajouter", None))
        self.delete_button.setText(QCoreApplication.translate("ContactsManager", u"Supprimer", None))
        self.name_input.setPlaceholderText(QCoreApplication.translate("ContactsManager", u"Nom", None))
        self.prenom_input.setPlaceholderText(QCoreApplication.translate("ContactsManager", u"Pr\u00e9nom (facultatif)", None))
        self.telephone_input.setPlaceholderText(QCoreApplication.translate("ContactsManager", u"T\u00e9l\u00e9phone (facultatif)", None))
        self.email_input.setPlaceholderText(QCoreApplication.translate("ContactsManager", u"Email (facultatif)", None))
    # retranslateUi

