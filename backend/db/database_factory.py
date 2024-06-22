"""
DatabaseFactory class that can create and return different types
of database connection instances (e.g., SQLite, PostgreSQL, MySQL).
"""

from abc import ABC, abstractmethod
from db.database_connections import SQLiteConnection, PostgreSQLConnection
import os


class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection():
        """Create a Database Connection"""
        return NotImplementedError

    # @abstractmethod
    def engine():
        """Create a Database Engine"""
        return NotImplementedError

class CreateDatabaseConnection(DatabaseFactory):
        def __init__(self, db_factory=object):
          self.db_factory = db_factory

        def create_connection(self):
            return self.db_factory.connection()

        def engine(self):
            return self.db_factory.engine


def get_session():
    """Return DB Session"""
    if os.environ.get('DB') == 'PostgreSQL':
        connection = CreateDatabaseConnection(db_factory=PostgreSQLConnection('db/db_config.json')).create_connection()
    elif os.environ.get('DB', 'SQLite') == 'SQLite':
        connection = CreateDatabaseConnection(db_factory=SQLiteConnection('db/db_config.json')).create_connection()
    else:
        raise ValueError("Unsupported database type")

    with connection as session:
        yield session

def get_engine():
    """Return DB Engine"""
    if os.environ.get('DB') == 'PostgreSQL':
        engine = CreateDatabaseConnection(db_factory=PostgreSQLConnection('db/db_config.json')).engine()
    elif os.environ.get('DB', 'SQLite') == 'SQLite':
        engine = CreateDatabaseConnection(db_factory=SQLiteConnection('db/db_config.json')).engine()
    return engine


