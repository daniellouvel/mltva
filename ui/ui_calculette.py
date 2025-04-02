# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calculette.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(395, 151)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(12, 12, 372, 128))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEditmnttva1 = QLineEdit(self.widget)
        self.lineEditmnttva1.setObjectName(u"lineEditmnttva1")

        self.gridLayout_2.addWidget(self.lineEditmnttva1, 0, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)

        self.lineEditmnttva2 = QLineEdit(self.widget)
        self.lineEditmnttva2.setObjectName(u"lineEditmnttva2")

        self.gridLayout_2.addWidget(self.lineEditmnttva2, 0, 3, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.comboBoxtva1 = QComboBox(self.widget)
        self.comboBoxtva1.addItem("")
        self.comboBoxtva1.addItem("")
        self.comboBoxtva1.addItem("")
        self.comboBoxtva1.addItem("")
        self.comboBoxtva1.setObjectName(u"comboBoxtva1")

        self.gridLayout_2.addWidget(self.comboBoxtva1, 1, 1, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)

        self.comboBoxtva2 = QComboBox(self.widget)
        self.comboBoxtva2.addItem("")
        self.comboBoxtva2.addItem("")
        self.comboBoxtva2.addItem("")
        self.comboBoxtva2.addItem("")
        self.comboBoxtva2.setObjectName(u"comboBoxtva2")

        self.gridLayout_2.addWidget(self.comboBoxtva2, 1, 3, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.labelttc1 = QLabel(self.widget)
        self.labelttc1.setObjectName(u"labelttc1")

        self.gridLayout_2.addWidget(self.labelttc1, 2, 1, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 2, 1, 1)

        self.labelttc2 = QLabel(self.widget)
        self.labelttc2.setObjectName(u"labelttc2")

        self.gridLayout_2.addWidget(self.labelttc2, 2, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.labeltotalttc = QLabel(self.widget)
        self.labeltotalttc.setObjectName(u"labeltotalttc")

        self.gridLayout.addWidget(self.labeltotalttc, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Tva 1 : ", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Tva 2 : ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Taux 1 : ", None))
        self.comboBoxtva1.setItemText(0, QCoreApplication.translate("Form", u"0%", None))
        self.comboBoxtva1.setItemText(1, QCoreApplication.translate("Form", u"5.5%", None))
        self.comboBoxtva1.setItemText(2, QCoreApplication.translate("Form", u"10%", None))
        self.comboBoxtva1.setItemText(3, QCoreApplication.translate("Form", u"20%", None))

        self.label_6.setText(QCoreApplication.translate("Form", u"Taux 2 : ", None))
        self.comboBoxtva2.setItemText(0, QCoreApplication.translate("Form", u"0%", None))
        self.comboBoxtva2.setItemText(1, QCoreApplication.translate("Form", u"5.5%", None))
        self.comboBoxtva2.setItemText(2, QCoreApplication.translate("Form", u"10%", None))
        self.comboBoxtva2.setItemText(3, QCoreApplication.translate("Form", u"20%", None))

        self.label.setText(QCoreApplication.translate("Form", u"TTC 1 :", None))
        self.labelttc1.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"TTC2 : ", None))
        self.labelttc2.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Total TTC : ", None))
        self.labeltotalttc.setText(QCoreApplication.translate("Form", u"0", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Validation ", None))
    # retranslateUi

