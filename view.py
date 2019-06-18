from web_app import app
from web_app import db_connection
from flask import render_template

@app.route("/")
def index():
    title = "Стартовая страница"
    content_title = "Выбор акции."
    content = "Вам необходимо выбрать финансовый инструмент для того, что бы увидеть сформированное по нему предсказание:"
#    content = "Для формирования предсказания по акции, выберите
#  из сниска ниже, интересующий Вас финансовый инструмент"

    stocks_list = db_connection.get_stocks_list()
    my_list = []
    for one_stock in stocks_list:
        my_list = my_list + [[one_stock[0], one_stock[2]]]

    ret_value = render_template("index.html", title=title, content_title=content_title, content=content, html_list=my_list)

    return(ret_value)
