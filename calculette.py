# calculette.py
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from PySide6.QtCore import Qt  # Importer Qt pour utiliser les constantes
from ui.ui_calculette import Ui_Form  # Importer l'interface générée

class CalculetteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()  # Créer une instance de l'interface
        self.ui.setupUi(self)  # Configurer l'interface

        # Connecter les signaux de changement de texte et de sélection
        self.ui.lineEditmnttva.textChanged.connect(self.calculate)
        self.ui.comboBoxtva.currentTextChanged.connect(self.calculate)

        # Configurer la fenêtre pour qu'elle soit toujours au premier plan
        self.setWindowModality(Qt.ApplicationModal)  # Rendre la fenêtre modale
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Toujours au-dessus

    def calculate(self):
        """Effectue le calcul du montant TTC à partir du montant de la TVA et du taux de TVA."""
        try:
            # Récupérer le montant de la TVA payé
            tva_paid = float(self.ui.lineEditmnttva.text())  # Montant de la TVA
            # Récupérer le taux de TVA sélectionné
            tva_rate = float(self.ui.comboBoxtva.currentText().strip('%'))  # Taux TVA

            # Calculer le montant TTC
            ttc = tva_paid / (tva_rate / 100) + tva_paid  # Formule pour calculer le montant TTC
            self.ui.labelttc.setText(f"{ttc:.2f}")  # Afficher le montant TTC

        except ValueError:
            self.ui.labelttc.setText("0")  # Réinitialiser le label TTC en cas d'erreur

# Point d'entrée pour exécuter la calculette seule
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = CalculetteDialog()
    dialog.show()  # Afficher la fenêtre de la calculette
    sys.exit(app.exec())