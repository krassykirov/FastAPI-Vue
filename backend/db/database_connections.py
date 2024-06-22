import json
from abc import ABC, abstractmethod
from sqlmodel import Session, SQLModel, create_engine

class Database(ABC):
    @abstractmethod
    def type(self):
        """DB Type"""

    @abstractmethod
    def _load_config(config_file):
        """Load config"""

    @abstractmethod
    def connection(engine):
        """Connect to db return Session"""


class SQLiteConnection(Database):
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.config = self._load_config(config_file)
        self.db_name = self.config["SQLIte"]["db_name"]
        self.database_url = f"sqlite:///{self.db_name}"
        self.engine = create_engine(
            self.database_url, connect_args={"check_same_thread": False}
        )

    def connection(self):
        return Session(self.engine)

    def _load_config(self, config_file):
        with open(config_file, "r") as f:
            return json.load(f)

    @property
    def type(self):
        print("SQLiteConnection")


class PostgreSQLConnection(Database):
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.config = self._load_config(config_file)
        self.database_url = (
            f'postgresql://{self.config["PostgreSQL"]["username"]}:'
            f'{self.config["PostgreSQL"]["password"]}@'
            f'{self.config["PostgreSQL"]["host"]}:'
            f'{self.config["PostgreSQL"]["port"]}/'
            f'{self.config["PostgreSQL"]["database"]}'
        )
        self.engine = create_engine(self.database_url)

    def connection(self):
        return Session(self.engine)


    def _load_config(self, config_file):
        with open(config_file, "r") as f:
            return json.load(f)

    @property
    def type(self):
        print("PostgreSQLConnection")
