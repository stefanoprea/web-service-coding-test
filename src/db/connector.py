from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


def DBConnector(database_url):
    if database_url.startswith("sqlite"):
        return SqliteConnector(database_url)
    elif database_url.startswith("postgre"):
        return PostgreConnector(database_url)
    else:
        # don't show the url, for security reasons
        raise Exception("Unsupported database url")


class DBConnectorBase:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = self._setup_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _setup_engine(self, database_url):
        return create_engine(database_url)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


class PostgreConnector(DBConnectorBase):
    pass


class SqliteConnector(DBConnectorBase):
    def _setup_engine(self, database_url):
        return create_engine(
            database_url, connect_args={"check_same_thread": False}
        )

    def get_db(self):
        db = self.SessionLocal()
        try:
            db.execute("PRAGMA foreign_keys=ON")
            yield db
        finally:
            db.close()
