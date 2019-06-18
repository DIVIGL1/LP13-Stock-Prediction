from flask import Blueprint
from flask import render_template

import db

predicts = Blueprint("predicts", __name__, template_folder="templates")

if "db_connection" not in locals():
    db_connection = db.Data_handler()


@predicts.route("/")
def index():
    return(render_template("predicts/index.html"))

@predicts.route("/<trade_kod>")
def predict_detail(trade_kod):
    stocks_list = db_connection.get_stocks_list()
    for one_stock in stocks_list:
        if one_stock[0]==trade_kod:
            stoks_full_name = one_stock[2]
            stoks_short_name = one_stock[3]
            break

    return(render_template("predicts/priction_page.html", trade_kod=trade_kod, stoks_full_name=stoks_full_name, stoks_short_name=stoks_short_name))
