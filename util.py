from constants import DB_CONFIG, ERROR_MESSAGES, UI_CONFIG
from database import DatabaseManager
from PySide6.QtWidgets import QMessageBox
from typing import Optional

# Ligne de débogage pour confirmer le chargement du module
print("Chargement du module util.py")

MOIS_NUMERIQUE_MAP = {
    "Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04",
    "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08",
    "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"
}

def convert_month_to_number(mois: str) -> int:
    """
    Convertit un mois en son numéro correspondant.
    :param mois: Nom du mois (str).
    :return: Numéro du mois (int).
    """
    return int(MOIS_NUMERIQUE_MAP.get(mois, "01"))


class PeriodeManager:
    def __init__(self, db_path=None):
        """
        Initialise le gestionnaire de période.
        :param db_path: Chemin vers la base de données SQLite.
        """
        self.db_manager = DatabaseManager(db_path)
        self.mois = None
        self.annee = None
        self.load_periode()

    def load_periode(self):
        """
        Charge la période actuelle depuis la base de données.
        """
        try:
            self.mois, self.annee = self.db_manager.load_periode()
            print(ERROR_MESSAGES["PERIODE_LOADED"].format(self.mois, self.annee))
        except Exception as e:
            print(ERROR_MESSAGES["PERIODE_LOAD_ERROR"].format(e))
            self.mois, self.annee = DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"]

    def get_periode(self):
        """
        Retourne la période actuelle sous forme de tuple (mois, année).
        """
        return self.mois, self.annee

    def convert_month_to_number(self, mois):
        """Convertit un mois en numéro."""
        mois_dict = {
            "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4,
            "Mai": 5, "Juin": 6, "Juillet": 7, "Août": 8,
            "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12
        }
        return mois_dict.get(mois, 1)


def calculate_tva(montant_ttc_text: str, tva_rate_text: str) -> Optional[float]:
    """
    Calcule le montant de la TVA à partir du montant TTC et du taux de TVA.
    :param montant_ttc_text: Montant TTC (str).
    :param tva_rate_text: Taux de TVA (str, format 'X%').
    :return: Montant de la TVA (float) ou None en cas d'erreur.
    """
    try:
        if not montant_ttc_text.replace('.', '', 1).isdigit():
            return None
        montant_ttc = float(montant_ttc_text)
        if not tva_rate_text.endswith('%'):
            return None
        tva_rate = float(tva_rate_text.strip('%'))
        montant_tva = montant_ttc * (tva_rate / (100 + tva_rate))
        return round(montant_tva, 2)
    except Exception as e:
        print(f"Erreur lors du calcul de la TVA : {e}")
        return None


def validate_fields(*fields):
    """
    Vérifie si tous les champs obligatoires sont remplis.
    :param fields: Liste des valeurs des champs (list).
    :return: True si tous les champs sont remplis, False sinon.
    """
    return all(fields)


def update_button_color(button, is_valid):
    """
    Change la couleur d'un bouton en fonction de la validité des champs.
    :param button: Bouton à modifier (QPushButton).
    :param is_valid: Booléen indiquant si les champs sont valides.
    """
    if is_valid:
        button.setStyleSheet("background-color: green; color: white;")
    else:
        button.setStyleSheet("")


def configure_fournisseur_combobox(combo_box, db_manager):
    """
    Configure un QComboBox avec la liste des fournisseurs.
    :param combo_box: QComboBox à configurer.
    :param db_manager: Instance de DatabaseManager pour accéder à la base de données.
    """
    combo_box.setEditable(True)
    combo_box.clear()
    query = "SELECT DISTINCT nom FROM contacts ORDER BY nom ASC"
    rows = db_manager.fetch_all(query)
    fournisseurs = [row['nom'] for row in rows if row['nom']]
    combo_box.addItems(fournisseurs)
    combo_box.setCurrentIndex(-1)


def handle_exception(e, message="Une erreur est survenue"):
    """
    Gère les exceptions globales et affiche un message d'erreur.
    :param e: L'exception levée.
    :param message: Message d'erreur personnalisé.
    """
    print(f"{message}: {str(e)}")
    return False