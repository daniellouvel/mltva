import sqlite3
from sqlite3 import Error
from constants import DB_CONFIG, ERROR_MESSAGES

class DatabaseManager:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls, db_file=None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_file=None):
        """Initialise la connexion à la base de données."""
        if db_file is None:
            db_file = DB_CONFIG["DEFAULT_PATH"]
        self.db_file = db_file
        self._conn = None
        self._cursor = None

    @property
    def conn(self):
        """Propriété qui gère le Lazy Loading de la connexion."""
        if self._conn is None:
            self._conn = self.create_connection()
        return self._conn

    @property
    def cursor(self):
        """Propriété qui gère le Lazy Loading du curseur."""
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    def create_connection(self):
        """Crée une connexion à la base de données SQLite."""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            # Optimisation des performances
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA cache_size = -2000")  # 2MB de cache
            print(ERROR_MESSAGES["DB_CONNECTION"])
            return conn
        except Error as e:
            print(ERROR_MESSAGES["DB_CONNECTION_ERROR"].format(e))
            return None

    def close_connection(self):
        """Ferme la connexion à la base de données."""
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def load_periode(self):
        """Charge les valeurs de la table 'periode' pour l'id = 1."""
        query = "SELECT mois, annee FROM periode WHERE id = 1"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                return str(result['mois']), str(result['annee'])
            else:
                self.save_periode(DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"])
                return DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"]
        except Error as e:
            print(ERROR_MESSAGES["DATABASE_ERROR"])
            return DB_CONFIG["DEFAULT_MONTH"], DB_CONFIG["DEFAULT_YEAR"]

    def save_periode(self, mois, annee):
        """Sauvegarde les valeurs de mois et année dans la table 'periode'."""
        query = """
        INSERT OR REPLACE INTO periode (id, mois, annee)
        VALUES (?, ?, ?)
        """
        return self.execute_query(query, (1, mois, annee))

    def fetch_all(self, query, params=None):
        """Exécute une requête SELECT et retourne toutes les lignes."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(ERROR_MESSAGES["DATABASE_ERROR"])
            return []

    def execute_query(self, query, params=None):
        """Exécute une requête SQL (INSERT, UPDATE, DELETE)."""
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return True
        except Error as e:
            print(ERROR_MESSAGES["DATABASE_ERROR"])
            return False

    def __del__(self):
        """Destructeur qui ferme la connexion à la base de données."""
        self.close_connection()

    # Méthodes pour gérer les dépenses
    def insert_depense(self, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire):
        """Insère une nouvelle dépense dans la table 'depenses'."""
        query = """
        INSERT INTO depenses (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire))

    def update_depense(self, id, date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire):
        """Met à jour une dépense existante dans la table 'depenses'."""
        query = """
        UPDATE depenses
        SET date=?, fournisseur=?, ttc=?, tva_id=?, montant_tva=?, validation=?, commentaire=?
        WHERE id=?
        """
        return self.execute_query(query, (date, fournisseur, ttc, tva_id, montant_tva, validation, commentaire, id))

    def delete_depense(self, id):
        """Supprime une dépense existante de la table 'depenses'."""
        query = "DELETE FROM depenses WHERE id=?"
        return self.execute_query(query, (id,))

    def update_validation_status(self, item_id, status):
        """Met à jour l'état de validation d'une dépense."""
        query = "UPDATE depenses SET validation = ? WHERE id = ?"
        return self.execute_query(query, (status, item_id))  # Utilisez des paramètres pour éviter les injections SQL

    # Méthodes pour gérer les recettes
    def insert_recette(self, date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire):
        """Insère une nouvelle recette dans la table 'recettes'."""
        query = """
        INSERT INTO recettes (date, client, paiement, numero_facture, montant, tva, montant_tva, commentaire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire))

    def update_recette(self, recette_id, date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire):
        """Met à jour une recette existante dans la table 'recettes'."""
        query = """
        UPDATE recettes
        SET date=?, client=?, paiement=?, numero_facture=?, montant=?, tva=?, montant_tva=?, commentaire=?
        WHERE id=?
        """
        return self.execute_query(query, (date, client, paiement, numero_facture, montant, tva_rate, montant_tva, commentaire, recette_id))

    def delete_recette(self, recette_id):
        """Supprime une recette existante de la table 'recettes'."""
        query = "DELETE FROM recettes WHERE id=?"
        return self.execute_query(query, (recette_id,))

    def fournisseur_exists(self, fournisseur):
        """Vérifie si le fournisseur existe déjà dans la table 'contacts'."""
        query = "SELECT COUNT(*) FROM contacts WHERE nom = ?"
        result = self.fetch_all(query, (fournisseur,))
        if result:  # Vérifiez si le résultat n'est pas vide
            return result[0][0] > 0  # Retourne True si le fournisseur existe
        return False  # Retourne False si aucun résultat

    def insert_fournisseur(self, nom):
        """Insère un nouveau fournisseur dans la table 'contacts'."""
        query = "INSERT INTO contacts (nom) VALUES (?)"
        return self.execute_query(query, (nom,))

    def client_exists(self, client):
        """Vérifie si le client existe déjà dans la table 'contacts'."""
        query = "SELECT COUNT(*) FROM contacts WHERE nom = ?"
        result = self.fetch_all(query, (client,))
        if result:  # Vérifiez si le résultat n'est pas vide
            return result[0][0] > 0  # Retourne True si le client existe
        return False  # Retourne False si aucun résultat

    def insert_client(self, nom, prenom=None, telephone=None, email=None):
        """Insère un nouveau client dans la table 'contacts'."""
        query = "INSERT INTO contacts (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)"
        return self.execute_query(query, (nom, prenom, telephone, email))

    def get_contact_id(self, nom):
        """Récupère l'ID d'un contact basé sur son nom."""
        query = "SELECT id FROM contacts WHERE nom = ?"
        result = self.fetch_all(query, (nom,))
        return result[0][0] if result else None

    def update_contact(self, contact_id, nom, prenom, telephone, email):
        """Met à jour un contact dans la table 'contacts'."""
        query = "UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, email = ? WHERE id = ?"
        return self.execute_query(query, (nom, prenom, telephone, email, contact_id))

    def delete_contact(self, contact_id):
        """Supprime un contact de la table 'contacts'."""
        query = "DELETE FROM contacts WHERE id = ?"
        return self.execute_query(query, (contact_id,))