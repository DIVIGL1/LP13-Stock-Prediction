from flask import Flask
from config import Configuraton

from predicts.blueprint import predicts

import db

app = Flask(__name__)
app.config.from_object(Configuraton)

if "db_connection" not in locals():
    db_connection = db.Data_handler()

app.register_blueprint(predicts, url_prefix="/predicts")
