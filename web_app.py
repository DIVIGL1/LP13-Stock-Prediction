from flask import Flask
from config import Configuraton


app = Flask(__name__)
app.config.from_object(Configuraton)
