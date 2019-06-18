from web_app import app
from flask import render_template

@app.route("/")
def index():
    title = "Стартовая страница"
    content_title = "Выбор акции."
    content = "Вам необходимо выбрать финансовый инструмент для того, что бы увидеть сформированное по нему предсказание:"
#    content = "Для формирования предсказания по акции, выберите
#  из сниска ниже, интересующий Вас финансовый инструмент"

    my_list = [["http://ya.ru", "ya.ru"]]
    my_list = my_list + [["http://yandex.ru", "yandex.ru"]]
    my_list = my_list + [["http://google.com", "Google"]]
    my_list = my_list + [["https://www.youtube.com/", "YouTube"]]

    ret_value = render_template("index.html", title=title, content_title=content_title, content=content, html_list=my_list)

    return(ret_value)
