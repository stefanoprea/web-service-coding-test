from config import database_url
from controllers.controllers import App
from db.connector import DBConnector


db_connector = DBConnector(database_url)
app = App(db_connector)
