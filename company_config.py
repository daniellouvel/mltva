"""
Configuration entreprise — chargée depuis company.json au démarrage.

Pour déployer chez une autre entreprise :
  1. Éditer company.json (name, legal, logo, db_name, backup_dir)
  2. Remplacer data/Logo.jpg par le logo de l'entreprise
  3. Relancer l'application

Si company.json est absent, les valeurs MLTVA sont utilisées par défaut.
"""

import json
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_FILE = os.path.join(_BASE_DIR, "company.json")

_DEFAULTS = {
    "name": "MLTVA",
    "legal": "MLTVA SARL",
    "logo": "data/Logo.jpg",
    "db_name": "mlbdd.db",
    "backup_dir": "data/backups",
    "address": "",
    "postal_code": "",
    "city": "",
    "phone": "",
    "email": "",
    "siret": "",
    "tva_intra": "",
}


def _load() -> dict:
    if os.path.exists(_CONFIG_FILE):
        try:
            with open(_CONFIG_FILE, encoding="utf-8") as f:
                data = json.load(f)
            return {**_DEFAULTS, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(_DEFAULTS)


COMPANY: dict = _load()


def reload() -> None:
    """Recharge company.json et met à jour COMPANY en place (sans réimporter)."""
    COMPANY.clear()
    COMPANY.update(_load())


def get_logo_path() -> str:
    """Chemin absolu vers le logo (gère les chemins absolus et relatifs)."""
    logo = COMPANY["logo"]
    if os.path.isabs(logo):
        return logo
    return os.path.join(_BASE_DIR, logo)


def get_db_path() -> str:
    """Chemin absolu vers la base de données principale."""
    return os.path.join(_BASE_DIR, "data", COMPANY["db_name"])


def get_backup_dir() -> str:
    """Chemin absolu vers le répertoire de sauvegardes."""
    return os.path.join(_BASE_DIR, COMPANY["backup_dir"])
