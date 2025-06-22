# Constants.py - Centralisation des constantes et messages

# Messages d'erreur
ERROR_MESSAGES = {
    "INVALID_DATE": "Le format de la date est incorrect (jj/mm/aaaa).",
    "MISSING_FIELDS": "Veuillez remplir tous les champs obligatoires.",
    "DATABASE_ERROR": "Une erreur est survenue lors de l'accès à la base de données.",
    "ADD_SUCCESS": "L'élément a été ajouté avec succès.",
    "UPDATE_SUCCESS": "L'élément a été modifié avec succès.",
    "DELETE_SUCCESS": "L'élément a été supprimé avec succès.",
    "NO_SELECTION": "Aucune ligne sélectionnée.",
    "INVALID_AMOUNT": "Le montant doit être un nombre valide.",
    "INVALID_TVA": "Le taux de TVA doit être un nombre valide.",
    "DB_CONNECTION": "Connexion à la base de données établie.",
    "DB_CONNECTION_ERROR": "Erreur de connexion à la base de données : {}",
    "PERIODE_LOADED": "Période chargée : {}, {}",
    "PERIODE_LOAD_ERROR": "Erreur lors du chargement de la période : {}"
}

# Configuration de la base de données
DB_CONFIG = {
    "DEFAULT_PATH": "data/mlbdd.db",
    "DEFAULT_MONTH": "Janvier",
    "DEFAULT_YEAR": "2023"
}

# Configuration de l'interface
UI_CONFIG = {
    "DATE_FORMAT": "%d/%m/%Y",
    "CALENDAR_VISIBLE": False,
    "DEFAULT_TVA_RATES": ["5.50%", "10.00%", "20.00%", "0.00%"]
}

# Messages de validation
VALIDATION_MESSAGES = {
    "REQUIRED_FIELDS": ["Date", "Fournisseur", "Montant", "TVA"],
    "DATE_FORMAT": "Format de date attendu : JJ/MM/AAAA",
    "AMOUNT_FORMAT": "Le montant doit être un nombre positif"
}