import os
import shutil
from datetime import datetime


DB_SOURCE = os.path.join("data", "mlbdd.db")
BACKUP_DIR = os.path.join("data", "backups")
MAX_DAILY = 10
MAX_MONTHLY = 12


def backup_database():
    """Crée les sauvegardes journalière, mensuelle et annuelle si nécessaire."""
    if not os.path.exists(DB_SOURCE):
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)

    today = datetime.now()
    _do_daily(today)
    _do_monthly(today)
    _do_annual(today)


def _copy(dest):
    shutil.copy2(DB_SOURCE, dest)


def _do_daily(today):
    name = f"mlbdd_{today.strftime('%Y-%m-%d')}.db"
    dest = os.path.join(BACKUP_DIR, name)
    if not os.path.exists(dest):
        _copy(dest)
        _cleanup_daily()


def _do_monthly(today):
    name = f"mlbdd_{today.strftime('%Y-%m')}.db"
    dest = os.path.join(BACKUP_DIR, name)
    if not os.path.exists(dest):
        _copy(dest)
        _cleanup_monthly()


def _do_annual(today):
    name = f"mlbdd_{today.strftime('%Y')}.db"
    dest = os.path.join(BACKUP_DIR, name)
    if not os.path.exists(dest):
        _copy(dest)


def _cleanup_daily():
    files = sorted(
        f for f in os.listdir(BACKUP_DIR)
        if len(f) == len("mlbdd_2026-05-02.db") and f.startswith("mlbdd_") and f[6:7].isdigit() and f[13:14] == "-"
    )
    for old in files[:-MAX_DAILY]:
        os.remove(os.path.join(BACKUP_DIR, old))


def _cleanup_monthly():
    files = sorted(
        f for f in os.listdir(BACKUP_DIR)
        if len(f) == len("mlbdd_2026-05.db") and f.startswith("mlbdd_") and f[6:7].isdigit() and "-" not in f[11:]
    )
    for old in files[:-MAX_MONTHLY]:
        os.remove(os.path.join(BACKUP_DIR, old))
