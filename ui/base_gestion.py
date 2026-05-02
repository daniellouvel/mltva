from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit, QComboBox
from PySide6.QtCore import Qt, QEvent, QDate
from util import calculate_tva, handle_exception


class GestionBase(QDialog):
    """Classe de base commune à GestionDepenses et GestionRecettes."""

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if isinstance(obj, (QLineEdit, QComboBox)):
                    return False
                if obj in (self.ui.quitterButton, self.ui.tableWidget):
                    return False
                self.add_new_row()
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if isinstance(self.focusWidget(), (QLineEdit, QComboBox)):
                return
            if self.focusWidget() in (self.ui.quitterButton, self.ui.tableWidget):
                return
            self.add_new_row()
        else:
            super().keyPressEvent(event)

    def show_calendar_on_focus(self, event):
        try:
            start_date = QDate(self.selected_year, self.selected_month, 1)
            if self.selected_month == 12:
                end_date = QDate(self.selected_year, 12, 31)
            else:
                next_month = QDate(self.selected_year, self.selected_month + 1, 1)
                end_date = next_month.addDays(-1)
            self.ui.calendarWidget.setMinimumDate(start_date)
            self.ui.calendarWidget.setMaximumDate(end_date)
            self.ui.calendarWidget.setVisible(True)
        except Exception as e:
            handle_exception(e, "Erreur lors de l'affichage du calendrier")

    def on_calendar_date_clicked(self, date):
        try:
            self.ui.lineEditDate.setText(f"{date.day():02d}/{date.month():02d}/{date.year()}")
            self.ui.calendarWidget.setVisible(False)
        except Exception as e:
            handle_exception(e, "Erreur lors de la sélection de la date")

    def calculate_tva(self):
        try:
            montant_tva = calculate_tva(self.ui.lineEditMontant.text(), self.ui.comboBoxTVA.currentText())
            if montant_tva is not None:
                self.ui.lineEditMontantTVA.setText(f"{montant_tva:.2f}")
            else:
                self.ui.lineEditMontantTVA.setText("")
        except Exception as e:
            handle_exception(e, "Erreur lors du calcul de la TVA")

    def calculate_and_update(self):
        try:
            tva_paid = float(self.ui.lineEditMontant.text())
            tva_rate = float(self.ui.comboBoxTVA.currentText().strip('%'))
            ttc = tva_paid / (tva_rate / 100) + tva_paid
            self.ui.lineEditMontantTVA.setText(f"{tva_paid:.2f}")
            self.ui.lineEditMontant.setText(f"{ttc:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un montant valide.")
