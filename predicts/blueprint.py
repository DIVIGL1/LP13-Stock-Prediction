import base64
from flask import Blueprint
from flask import make_response
from flask import render_template
import io
import matplotlib.pyplot as plt

import constants
import db

predicts = Blueprint("predicts", __name__, template_folder="templates")

if "db_connection" not in locals():
    db_connection = db.Data_handler()


@predicts.route("/")
def index():
    return(render_template("predicts/index.html"))

@predicts.route("/<inline_kod>")
def predict_detail(inline_kod):
    if inline_kod[:5]=="code_":
        trade_kod = inline_kod[5:]
        stocks_list = db_connection.get_stocks_list()
        for one_stock in stocks_list:
            if one_stock[0]==trade_kod:
                stoks_full_name = one_stock[2]
                stoks_short_name = one_stock[3]
                break
        my_list = [[f"plot_code_{trade_kod}_price_OPEN", "Цена открытия"]]
        my_list = my_list + [[f"plot_code_{trade_kod}_price_MIN", "Минимальная цена"]]
        my_list = my_list + [[f"plot_code_{trade_kod}_price_MAX", "Максимальная цена"]]
        my_list = my_list + [[f"plot_code_{trade_kod}_price_CLOSE", "Цена закрытия"]]

        return(render_template("predicts/description_page.html", html_list=my_list, trade_kod=trade_kod, stoks_full_name=stoks_full_name, stoks_short_name=stoks_short_name))
    elif inline_kod[:6]=="frame_":
        trade_kod = inline_kod[6:]
        return(render_template("predicts/frameset.html", trade_kod=trade_kod))
    elif inline_kod[:5]=="plot_":
        inline_kod = inline_kod[10:].split("_price_")
        trade_kod = inline_kod[0]
        price_type = inline_kod[1]
        return(render_template("predicts/plot_page.html", trade_kod=trade_kod, price_type=price_type))
    elif inline_kod[:5]=="pict_":
        inline_kod = inline_kod[10:].split("_price_")
        trade_kod = inline_kod[0]
        price_type = inline_kod[1].upper()
        
        mfd_id = get_id_for_code(trade_kod)
        df = db_connection.get_stocks_prices_pd(mfd_id=mfd_id, id_period_type=constants.PERIOD_TYPES["Час"], price_type=price_type, dt_begin="2019/01/01")
        _, ax = plt.subplots(figsize=(15, 4))
        ax.plot(df["price_dt"], df["price"], lw=2, color='#539caf', alpha=1)

        ax.set_title("График изменения стоимости акции")
        ax.set_xlabel("")
        ax.set_ylabel(f"Цена ({price_type})")

        img = io.BytesIO()
        plt.savefig(img, format='png')

        response = make_response(img.getvalue())
        response.headers['Content-Type'] = 'img/png'
        response.headers['Content-Length'] = len(img.getvalue())
        response.headers['Content-Disposition'] = 'inline; filename="%s"' % (inline_kod)
        img.close()

        return(response)

def get_id_for_code(trade_kod):
    stocks_list = db_connection.get_stocks_list()
    for one_stock in stocks_list:
        if one_stock[0]==trade_kod:
            mfd_id = one_stock[1]
            break
    return(mfd_id)


