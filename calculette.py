# calculette.py
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from PySide6.QtCore import Qt  # Importer Qt pour utiliser les constantes
from ui.ui_calculette import Ui_Form  # Importer l'interface générée
from constants import UI_CONFIG  # Importer UI_CONFIG

class CalculetteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()  # Créer une instance de l'interface
        self.ui.setupUi(self)  # Configurer l'interface

        # Initialiser comboBoxtva avec les valeurs de DEFAULT_TVA_RATES
        self.ui.comboBoxtva.addItems(UI_CONFIG["DEFAULT_TVA_RATES"])  # Ajouter les taux de TVA

        # Vérification des valeurs ajoutées
        print("Valeurs ajoutées à comboBoxtva:", [self.ui.comboBoxtva.itemText(i) for i in range(self.ui.comboBoxtva.count())])

        # Connecter les signaux de changement de texte et de sélection
        self.ui.lineEditmnttva.textChanged.connect(self.calculate)
        self.ui.comboBoxtva.currentTextChanged.connect(self.calculate)

        # Connecter le bouton de validation à la méthode de mise à jour et de fermeture
        self.ui.pushButton.clicked.connect(self.update_and_close)

        # Configurer la fenêtre pour qu'elle soit toujours au premier plan
        self.setWindowModality(Qt.ApplicationModal)  # Rendre la fenêtre modale
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Toujours au-dessus

    def set_initial_values(self, tva_value, montant_value=None):
        """Définit les valeurs initiales pour la calculette."""
        self.ui.comboBoxtva.setCurrentText(tva_value)  # Définir le taux de TVA
        if montant_value is not None:
            self.ui.lineEditmnttva.setText(montant_value)  # Définir le montant
        self.ui.lineEditmnttva.setFocus()  # Mettre le focus sur lineEditmnttva

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

    def update_and_close(self):
        """Met à jour le montant dans gestion_depenses.py et ferme la calculette."""
        try:
            # Récupérer la valeur de labelttc
            ttc_value = self.ui.labelttc.text()
            # Récupérer la valeur de comboBoxtva
            tva_rate = self.ui.comboBoxtva.currentText()

            print(f"Valeur de ttc_value: {ttc_value}, Valeur de tva_rate: {tva_rate}")

            # Mettre à jour lineEditMontant et comboBoxTVA dans gestion_depenses.py
            if self.parent():  # Vérifier si un parent est défini
                self.parent().ui.lineEditMontant.setText(ttc_value)  # Mettre à jour le montant
                self.parent().ui.comboBoxTVA.setCurrentText(tva_rate)  # Mettre à jour le taux de TVA

            self.close()  # Fermer la fenêtre de la calculette

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Erreur lors de la mise à jour du montant.")

# Point d'entrée pour exécuter la calculette seule
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = CalculetteDialog()
    dialog.show()  # Afficher la fenêtre de la calculette
    sys.exit(app.exec())