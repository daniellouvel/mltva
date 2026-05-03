import sqlite3
import logging
from contextlib import contextmanager
from sqlite3 import Error
from constants import DB_CONFIG, ERROR_MESSAGES

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton avec une seule connexion SQLite vers le chemin defini dans
    constants.DB_PATH. Les anciennes signatures DatabaseManager("...") restent
    acceptees pour compatibilite mais l argument est ignore : il y a un seul
    chemin pour toute l application.
    """
    _instance = None
    _initialized = False

    def __new__(cls, db_file=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_file=None):
        if DatabaseManager._initialized:
            return
        self.db_file = DB_CONFIG["DEFAULT_PATH"]
        self._conn = None
        self._cursor = None
        DatabaseManager._initialized = True

    # ── Connexion ─────────────────────────────────────────────────────────────

    @property
    def conn(self):
        if self._conn is None:
            self._conn = self._create_connection()
        return self._conn

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    def _create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA cache_size = -2000")
            conn.execute("PRAGMA foreign_keys = ON")
            self._migrate(conn)
            logger.info(ERROR_MESSAGES["DB_CONNECTION"])
            return conn
        except Error as e:
            logger.error(ERROR_MESSAGES["DB_CONNECTION_ERROR"].format(e))
            raise

    def _migrate(self, conn):
        """Appliquer les migrations de schéma manquantes (idempotent)."""
        cols = {row[1] for row in conn.execute("PRAGMA table_info(recettes)")}
        if "validation" not in cols:
            conn.execute("ALTER TABLE recettes ADD COLUMN validation TEXT DEFAULT 'Non'")
            conn.commit()

    # Compat : alias historique (utilise dans certaines vues)
    def create_connection(self):
        return self._create_connection()

    def close_connection(self):
        if self._cursor is not None:
            try:
                self._cursor.close()
            except Error:
                pass
            self._cursor = None
        if self._conn is not None:
            try:
                self._conn.close()
            except Error:
                pass
            self._conn = None

    def __del__(self):
        try:
            self.close_connection()
        except Exception:
            pass

    # ── Transactions atomiques ────────────────────────────────────────────────

    @contextmanager
    def transaction(self):
        """
        Contexte transactionnel : commit si tout passe, rollback en cas
        d exception. Permet d enchainer plusieurs ecritures atomiquement.

            with db.transaction() as cur:
                cur.execute(q1, p1)
                cur.execute(q2, p2)
        """
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Error:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    # ── Requetes generiques ───────────────────────────────────────────────────

    def fetch_all(self, query, params=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            return cur.fetchall()
        except Error as e:
            logger.error("fetch_all failed: %s", e)
            return []

    def fetch_one(self, query, params=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            return cur.fetchone()
        except Error as e:
            logger.error("fetch_one failed: %s", e)
            return None

    def execute_query(self, query, params=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, params or ())
            self.conn.commit()
            return True
        except Error as e:
            logger.error("execute_query failed: %s", e)
            try:
                self.conn.rollback()
            except Error:
                pass
            return False

    # ── Periode ───────────────────────────────────────────────────────────────

    def load_periode(self):
        query = "SELECT mois, annee FROM periode WHERE id = 1"
        try:
            row = self.fetch_one(query)
            if row:
                return str(row["mois"]), str(row["annee"])
            self.save_periode(DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"])
            return DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"]
        except Error:
            return DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"]

    def save_periode(self, mois, annee):
        query = "INSERT OR REPLACE INTO periode (id, mois, annee) VALUES (?, ?, ?)"
        return self.execute_query(query, (1, mois, annee))

    # ── Depenses ──────────────────────────────────────────────────────────────

    def insert_depense(self, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire):
        query = """
        INSERT INTO depenses (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire))

    def insert_depense_with_fournisseur(self, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire):
        """
        Atomique : cree le fournisseur s il n existe pas + insere la depense.
        Retourne True si tout passe, False sinon (rollback complet).
        """
        try:
            with self.transaction() as cur:
                cur.execute("SELECT 1 FROM contacts WHERE nom = ?", (fournisseur,))
                if not cur.fetchone():
                    cur.execute("INSERT INTO contacts (nom) VALUES (?)", (fournisseur,))
                cur.execute(
                    "INSERT INTO depenses (date, fournisseur, ttc, tva_id, "
                    "montant_tva, validation, commentaire) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)
                )
            return True
        except Error as e:
            logger.error("insert_depense_with_fournisseur failed: %s", e)
            return False

    def update_depense(self, id, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire):
        query = """
        UPDATE depenses
        SET date=?, fournisseur=?, ttc=?, tva_id=?, montant_tva=?, validation=?, commentaire=?
        WHERE id=?
        """
        return self.execute_query(query, (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire, id))

    def delete_depense(self, id):
        return self.execute_query("DELETE FROM depenses WHERE id=?", (id,))

    def update_validation_status(self, item_id, status):
        return self.execute_query("UPDATE depenses SET validation = ? WHERE id = ?", (status, item_id))

    def find_depense_doublons(self, ttc, fournisseur, mois, annee):
        """Doublons sur meme TTC + fournisseur + meme mois/annee."""
        query = """
            SELECT id, date, fournisseur, ttc FROM depenses
            WHERE ttc = ? AND fournisseur = ?
              AND strftime('%m', date) = ?
              AND strftime('%Y', date) = ?
        """
        return self.fetch_all(query, (ttc, fournisseur, f"{int(mois):02d}", str(annee)))

    # ── Recettes ──────────────────────────────────────────────────────────────

    def insert_recette(self, date, client, paiement, numero_facture, montant, tva_rate, montant_tva, validation, commentaire):
        query = """
        INSERT INTO recettes (date, client, paiement, numero_facture, montant, tva, montant_tva, validation, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (date, client, paiement, numero_facture, montant, tva_rate, montant_tva, validation, commentaire))

    def update_recette(self, recette_id, date, client, paiement, numero_facture, montant, tva_rate, montant_tva, validation, commentaire):
        query = """
        UPDATE recettes
        SET date=?, client=?, paiement=?, numero_facture=?, montant=?, tva=?, montant_tva=?, validation=?, commentaire=?
        WHERE id=?
        """
        return self.execute_query(query, (date, client, paiement, numero_facture, montant, tva_rate, montant_tva, validation, commentaire, recette_id))

    def delete_recette(self, recette_id):
        return self.execute_query("DELETE FROM recettes WHERE id=?", (recette_id,))

    # ── Contacts ──────────────────────────────────────────────────────────────

    def contact_exists(self, nom):
        query = "SELECT COUNT(*) FROM contacts WHERE nom = ?"
        result = self.fetch_all(query, (nom,))
        return bool(result and result[0][0] > 0)

    def fournisseur_exists(self, nom):
        return self.contact_exists(nom)

    def client_exists(self, nom):
        return self.contact_exists(nom)

    def insert_fournisseur(self, nom):
        return self.execute_query("INSERT INTO contacts (nom) VALUES (?)", (nom,))

    def insert_client(self, nom, prenom=None, telephone=None, email=None):
        query = "INSERT INTO contacts (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)"
        return self.execute_query(query, (nom, prenom, telephone, email))

    def get_contact_id(self, nom):
        result = self.fetch_all("SELECT id FROM contacts WHERE nom = ?", (nom,))
        return result[0][0] if result else None

    def update_contact(self, contact_id, nom, prenom, telephone, email):
        query = "UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, email = ? WHERE id = ?"
        return self.execute_query(query, (nom, prenom, telephone, email, contact_id))

    def delete_contact(self, contact_id):
        return self.execute_query("DELETE FROM contacts WHERE id = ?", (contact_id,))
