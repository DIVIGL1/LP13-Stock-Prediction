# -*- coding: utf-8 -*-

initual_data_PERIOD_TYPES = \
        {
            "table_name": "PERIOD_TYPES", "find_and_update_or_insert": True, "id_column": "id", "donot_commit": False,
                "data":
                [   {"id": 0, "period_name": "Один тик", "phidden": 1}, 
                    {"id": 1, "period_name": "Одна минута", "phidden": 1}, 
                    {"id": 2, "period_name": "5 минут", "phidden": 1}, 
                    {"id": 3, "period_name": "10 минут", "phidden": 1}, 
                    {"id": 4, "period_name": "15 минут", "phidden": 1}, 
                    {"id": 5, "period_name": "30 минут", "phidden": 1}, 
                    {"id": 6, "period_name": "Час", "phidden": 0}, 
                    {"id": 7, "period_name": "День", "phidden": 1}, 
                    {"id": 8, "period_name": "Неделя", "phidden": 1}, 
                    {"id": 9, "period_name": "Месяц", "phidden": 1} 
                ] 
        }

initual_data_STOCKS = \
        {
            "table_name": "STOCKS", "find_and_update_or_insert": True, "id_column": "trade_kod", "donot_commit": False,
                "data":
                [   {"trade_kod": "GAZP", "mfd_id": 330, "full_name": 'ПАО "Газпром", акция обыкновенная', "short_name": "ГАЗПРОМ а/о", "order_field": 1, "phidden": 0}, 
                    {"trade_kod": "LKOH", "mfd_id": 632, "full_name": 'ПАО "Нефтяная компания "ЛУКОЙЛ", акция обыкновенная', "short_name": "ЛУКОЙЛ а/о", "order_field": 2, "phidden": 0}, 
                    {"trade_kod": "MTLR", "mfd_id": 9060, "full_name": 'ПАО  "Мечел", акция обыкновенная', "short_name": "МЕЧЕЛ а/о", "order_field": 3, "phidden": 0}, 
                    {"trade_kod": "TGKB", "mfd_id": 1567, "full_name": 'ОАО "Территориальная генерирующая компания №2", а/о', "short_name": "ТГК-2 а/о", "order_field": 4, "phidden": 0}, 
                    {"trade_kod": "NSVZ", "mfd_id": 41928, "full_name": 'ПАО Многофункциональный оператор связи "Наука-Связь"', "short_name": "НаукаСвяз а/о", "order_field": 5, "phidden": 0} 
                ] 
        }

# Сгенерируем словарь с типами периодов:
PERIOD_TYPES = { 
                initual_data_PERIOD_TYPES["data"][j]["period_name"]: initual_data_PERIOD_TYPES["data"][j]["id"] 
                    for j in range(1, len(initual_data_PERIOD_TYPES["data"]))
               }

