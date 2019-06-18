from flask import Flask
from config import Configuraton

import db

app = Flask(__name__)
app.config.from_object(Configuraton)

if "db_connection" not in locals():
    db_connection = db.Data_handler()
    stocks_list = db_connection.get_stocks_list()
