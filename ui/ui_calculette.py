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
        Form.resize(243, 151)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(12, 12, 221, 128))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 3, 1, 1, 1)

        self.comboBoxtva = QComboBox(self.layoutWidget)
        self.comboBoxtva.setObjectName(u"comboBoxtva")

        self.gridLayout_2.addWidget(self.comboBoxtva, 1, 1, 1, 1)

        self.lineEditmnttva = QLineEdit(self.layoutWidget)
        self.lineEditmnttva.setObjectName(u"lineEditmnttva")

        self.gridLayout_2.addWidget(self.lineEditmnttva, 0, 1, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.labelttc = QLabel(self.layoutWidget)
        self.labelttc.setObjectName(u"labelttc")

        self.gridLayout_2.addWidget(self.labelttc, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Validation ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Taux :  ", None))
        self.label.setText(QCoreApplication.translate("Form", u"TTC :", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Mnt TVA : ", None))
        self.labelttc.setText(QCoreApplication.translate("Form", u"0", None))
    # retranslateUi

