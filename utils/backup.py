import os
import shutil
from datetime import datetime

from company_config import get_db_path, get_backup_dir

MAX_DAILY = 10
MAX_MONTHLY = 12


def backup_database():
    """Crée les sauvegardes journalière, mensuelle et annuelle si nécessaire."""
    db_source = get_db_path()
    backup_dir = get_backup_dir()

    if not os.path.exists(db_source):
        return

    os.makedirs(backup_dir, exist_ok=True)

    today = datetime.now()
    _do_daily(today, db_source, backup_dir)
    _do_monthly(today, db_source, backup_dir)
    _do_annual(today, db_source, backup_dir)


def _copy(db_source, dest):
    shutil.copy2(db_source, dest)


def _do_daily(today, db_source, backup_dir):
    name = f"mlbdd_{today.strftime('%Y-%m-%d')}.db"
    dest = os.path.join(backup_dir, name)
    if not os.path.exists(dest):
        _copy(db_source, dest)
        _cleanup_daily(backup_dir)


def _do_monthly(today, db_source, backup_dir):
    name = f"mlbdd_{today.strftime('%Y-%m')}.db"
    dest = os.path.join(backup_dir, name)
    if not os.path.exists(dest):
        _copy(db_source, dest)
        _cleanup_monthly(backup_dir)


def _do_annual(today, db_source, backup_dir):
    name = f"mlbdd_{today.strftime('%Y')}.db"
    dest = os.path.join(backup_dir, name)
    if not os.path.exists(dest):
        _copy(db_source, dest)


def _cleanup_daily(backup_dir):
    files = sorted(
        f for f in os.listdir(backup_dir)
        if len(f) == len("mlbdd_2026-05-02.db") and f.startswith("mlbdd_") and f[6:7].isdigit() and f[13:14] == "-"
    )
    for old in files[:-MAX_DAILY]:
        os.remove(os.path.join(backup_dir, old))


def _cleanup_monthly(backup_dir):
    files = sorted(
        f for f in os.listdir(backup_dir)
        if len(f) == len("mlbdd_2026-05.db") and f.startswith("mlbdd_") and f[6:7].isdigit() and "-" not in f[11:]
    )
    for old in files[:-MAX_MONTHLY]:
        os.remove(os.path.join(backup_dir, old))
