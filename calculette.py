# calculette.py
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class CalculetteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculette")
        self.setGeometry(200, 200, 300, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Widgets
        self.label_ht = QLabel("Montant HT:")
        self.input_ht = QLineEdit()
        self.label_tva = QLabel("Taux TVA (%):")
        self.input_tva = QLineEdit()
        self.result_label = QLabel("Résultat:")
        self.result_display = QLabel("")
        self.calculate_button = QPushButton("Calculer")

        # Ajout des widgets au layout
        layout.addWidget(self.label_ht)
        layout.addWidget(self.input_ht)
        layout.addWidget(self.label_tva)
        layout.addWidget(self.input_tva)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_display)
        layout.addWidget(self.calculate_button)

        # Définir le layout pour la fenêtre
        self.setLayout(layout)

        # Connecter les signaux
        self.calculate_button.clicked.connect(self.calculate)

    def calculate(self):
        """Effectue le calcul du montant TTC et de la TVA."""
        try:
            ht = float(self.input_ht.text())
            tva_rate = float(self.input_tva.text())
            tva_amount = ht * (tva_rate / 100)
            ttc = ht + tva_amount
            self.result_display.setText(f"TVA: {tva_amount:.2f}, TTC: {ttc:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer des valeurs numériques valides.")

    def get_values(self):
        """Retourne les valeurs calculées (TVA et TTC)."""
        result_text = self.result_display.text()
        if result_text:
            parts = result_text.split(", ")
            tva = float(parts[0].split(": ")[1])
            ttc = float(parts[1].split(": ")[1])
            return tva, ttc
        return None, None


# Point d'entrée pour exécuter la calculette seule
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = CalculetteDialog()
    if dialog.exec():
        tva, ttc = dialog.get_values()
        if tva is not None and ttc is not None:
            print(f"Valeurs calculées - TVA: {tva:.2f}, TTC: {ttc:.2f}")
    sys.exit(app.exec())