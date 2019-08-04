import datetime
import os

import sqlite3 as sqlite
import pandas as pd
from tqdm import tqdm

import src.config as config
import src.constants as constants
import src.utils as utils


class Data_handler():
    """ 
    При создании экземпляра данного класса будет создан обьект,
    который пощволяет управлять таблицами базы данных.
    При его создании если база данных отсуствует, то будет созданна,
    а справочники щаролнены.
    """
    def __init__(self):
        ''' 
        Объект класса позволяет работать с базой данных.
        '''
        self.get_connector()
        self.create_tables()
        
        # Добавим данные в справочники.
        # В PERIOD_TYPES:
        initual_data = constants.initual_data_PERIOD_TYPES
        self.add_rows_from_struct(initual_data)

        # В STOCKS:
        initual_data = constants.initual_data_STOCKS
        self.add_rows_from_struct(initual_data)


    def get_dbase_path(self):
        try:
            basedir = os.path.join(config.DB_FULL_PATH, "DBase")
            if not os.path.isdir(basedir): 
                os.makedirs(basedir)

            ret_path = os.path.join(basedir, "test.sqlight")
            return(ret_path)
        except:
            print("Не удалось подготовить информацию о расположении базы данных.")
            return("")
    
    def __del__(self):
        '''
        При уничтожении экземпляра класса 
        закрывается соединение с базой данных.
        '''
        self._connector.close()      #
        print("Закрыли соединение с БД.")


    def get_connector(self):
        '''
        Подключение к базе данных.
        '''
        try:
            self._connector = sqlite.connect(self.get_dbase_path(), check_same_thread=False)
        except (sqlite.Error):
            print("get_connector: Возникла проблема с подключением к базе данных.")
            if self._connector: self._connector.close()
            return (False)
        if self._connector:
            print("Установили соединение с БД.")
            return(True)
        else:
            print("get_connector: При установлении связи с БД возникли ошибки.")
            return(False)    
    
    def create_tables(self):   #функця создания таблиц
        '''
        Создание основных таблиц, их индексов, тригеров и заполнение справочников.
        '''
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS STOCKS (trade_kod TEXT NOT NULL PRIMARY KEY, mfd_id INTEGER NOT NULL, full_name TEXT NOT NULL, short_name TEXT NOT NULL, order_field INTEGER NOT NULL, phidden INTEGER NOT NULL)")
        except:
            print("create_tables: При создании таблицы STOCKS возникла ошибка.")
            return(False)
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS PERIOD_TYPES (id INTEGER PRIMARY KEY, period_name TEXT, phidden INTEGER)")
        except:
            print("create_tables: При создании таблицы PERIOD_TYPES возникла ошибка.")
            return(False)
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS STOCKS_PRICES (mfd_id INTEGER NOT NULL, price_dt TIMESTAMP NOT NULL, id_period_type INTEGER NOT NULL, price_open REAL NOT NULL, price_min REAL NOT NULL, price_max REAL NOT NULL, price_close REAL NOT NULL, vol INTEGER NOT NULL, ppredict INTEGER NOT NULL)")
            cur.execute("CREATE TRIGGER IF NOT EXISTS trig_STOCKS_PRICES_befor_insert BEFORE INSERT ON STOCKS_PRICES FOR EACH ROW BEGIN DELETE FROM STOCKS_PRICES WHERE mfd_id=NEW.mfd_id AND price_dt=NEW.price_dt AND id_period_type=NEW.id_period_type; END")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS unique_combination ON STOCKS_PRICES (mfd_id, price_dt, id_period_type)")
            cur.execute("CREATE INDEX IF NOT EXISTS ppredict ON STOCKS_PRICES (ppredict)")
        except:
            print("create_tables: При создании таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)

    
    def get_stocks_list(self): #выбор одного из инструментов
        '''
        Предоставление списка акций.
        '''
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT * FROM STOCKS WHERE phidden==0 ORDER BY order_field")
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)
    
    
    def get_period_types_list(self):
        '''
        Предоставление списка возможных периодов (временных шагов).
        '''
        if not self._connector:
            return(False)
        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT * FROM PERIOD_TYPES WHERE phidden==0 ORDER BY id")
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы PERIOD_TYPES возникла ошибка.")
            return(False)
        # Так как ошибок не было, то выходим с True
        return(True)       

    
    def add_rows_from_struct(self, data):
        '''
        Добавление в таблицу данных представленных в виде специализированный структуры.
        '''
        ret_code = True
        for one_row in data["data"]:
            ret_code = self.add_row(data["table_name"], one_row, find_and_update_or_insert=data["find_and_update_or_insert"], id_column=data["id_column"], donot_commit=data["donot_commit"])
            if not ret_code: break
        return(ret_code)


    def add_row(self, table_name, data, find_and_update_or_insert=False, id_column="", donot_commit=False):
        ''' 
        Данная функция предназеачена для ввода даных по одной строке.
        данные добавляются в таблице имя которой передано в параметре <table_name>.
        Имя столбца идентификатора в таблице передается в параметре <id_column>.
        Если параметр <find_and_update_or_insert>= False то переданные даннае добавляются как новая строка.
        Если параметр <find_and_update_or_insert>= True то сначала делается попытка
        найти строку с соответствующим идентификатором. если такая строка найдена то она обновляется,
        а если не найдена то добавляется новая строка.
        Если параметр <donot_commit>=True то по завершении метода commit не делается.
        '''
        if not self._connector:
            print("add_row: У данного объекта отсутствует коннектор.")
            return(False)


        table_name = table_name.replace(" ","").upper()
        cur = self._connector.cursor()
        if find_and_update_or_insert:
            # Ветка "НайдиИОбнови".
            # Предварительно нужно проверить, если такая запись уже есть, то её нужно не добавить а обновить.
            if id_column=="":
                print("add_row: Необходимо проверить наличие в таблице {} строки с идентификатором, а имя идентификатора не передано.".format(table_name))
                return(False)
            else:
                cur.execute("SELECT COUNT(*) FROM {} WHERE {}=?".format(table_name,id_column), ( data[id_column], ) )
                if cur.fetchone()[0]==1:
                    try:
                        cur = self._connector.cursor()
                        if table_name=="STOCKS":
                            cur.execute("UPDATE {} SET full_name=?, short_name=?, order_field=?, phidden=? WHERE {}=?".format(table_name,id_column), \
                                ( data["full_name"], data["short_name"], data["order_field"], data["phidden"], data["trade_kod"] ) )
                        elif table_name=="PERIOD_TYPES":
                            cur.execute("UPDATE {} SET period_name=?, phidden=? WHERE {}=?".format(table_name,id_column), \
                                ( data["period_name"], data["phidden"], data["id"] ) )
                        elif table_name=="STOCKS_PRICES":
                            print("add_row: Попытка обновить данные в таблице: " + table_name + ". Эта операция не предусмотрена структурой данных.")
                            return(False)
                        else:
                            print("add_row: Попытка обновить данные в несуществующей таблице: " + table_name)
                            return(False)
                    except:
                        print("add_row: При обновлении существующей строки в таблице {} возникла ошибка.".format(table_name))
                        self._connector.rollback()
                        return(False)
                    if not donot_commit:
                        self._connector.commit()
                    # Так как это была ветка "НайдиИОбнови" и ошибок не произошло, то на этом завершаем работу и выходим с True.
                    return(True)

        # Ветка "ДобавьНовыеДанные"
        try:
            if table_name=="STOCKS":
                cur.execute("INSERT INTO STOCKS (trade_kod, mfd_id, full_name, short_name, order_field, phidden) VALUES(?, ?, ?, ?, ?, ?)", \
                    ( data["trade_kod"], data["mfd_id"], data["full_name"], data["short_name"], data["order_field"], data["phidden"] ) )
            elif table_name=="PERIOD_TYPES":
                cur.execute("INSERT INTO PERIOD_TYPES (id, period_name, phidden) VALUES(?, ?, ?)", \
                    ( data["id"], data["period_name"], data["phidden"] ) )
            elif table_name=="STOCKS_PRICES":
                cur.execute("INSERT INTO STOCKS_PRICES (mfd_id, price_dt, id_period_type, price_open, price_min, price_max, price_close, vol, ppredict) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                    ( data["mfd_id"], data["price_dt"], data["id_period_type"], data["price_open"], data["price_min"], data["price_max"], data["price_close"], data["vol"], data["ppredict"] ) )
            else:
                print("add_row: Попытка добавить данные в несуществующую таблицу: " + table_name)
                return(False)
        except:
            print("add_row: При добавлении строки в таблицу {} возникла ошибка.".format(table_name))
            self._connector.rollback()
            return(False)

        if not donot_commit: self._connector.commit()
        # Так как ошибок не было, то выходим с True
        return(True)


    def get_stocks_prices_pd(self, mfd_id, id_period_type=constants.DEFAULT_PERIOD_TYPE, price_type="MAX", dt_begin="", dt_end="", ppredict=0): 
        '''
        Выборка цен на акцию по условию и предоставление данных в формате Pandas DataFrame.
        '''
        if not self._connector:
            return(False)
        dt_begin, dt_end = self._prepare_dates(dt_begin, dt_end)        
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT price_dt, price_{} AS price, vol FROM STOCKS_PRICES WHERE mfd_id=? and id_period_type=? AND ppredict=? AND price_dt BETWEEN ? AND ? ORDER BY price_dt".format(price_type.lower()), (mfd_id, id_period_type, ppredict, dt_begin, dt_end))
            return(pd.DataFrame(cur.fetchall(), columns=["price_dt", "price", "vol"]))
        except:
            print("get_stocks_list: При попытке получить выборку из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)


    def load_stock_prises_from_file2df(self, file_name):    # Вынрузка данных из файла "file_name"
        '''
        Загрузка информации о ценах из локального файла в формат Pandas DataFrame.
        '''
        if not os.path.isfile(file_name):
            print("load_stock_prises_from_file: Файл '{}' не найден.".format(file_name))
            return(False)

        print("Получаем данные о стоимости акций из текстового файла '{}'".format(file_name))
        df = pd.read_csv(file_name, sep=";")
        # Полученную таблицу нужно причесать:
        return(utils.prepare_df(df))


    def load_stock_prises_from_df2db(self, mfd_id, id_period_type, df): #добавляем данные в БД
        '''
        Загрузка цен акций в базу данных из таблицы в формате Pandas DataFrame.
        '''
        try:
            rows_ko_bo = df.shape[0]
        except:
            print("load_stock_prises_from_df2db: Проблема с исходными данными.")
            return(False)
        print("Загрузка цен на акции в DBase. Количество строк для загрузки: {}".format(rows_ko_bo))
        if rows_ko_bo==0:
            return(0)
        else:
            p_all_transactions_good = True
            for _, row in tqdm(df.iterrows(), total=df.shape[0]):
                # Добавим строчки по одной в STOCKS_PRICES:
                initual_data = {"table_name": "STOCKS_PRICES", "find_and_update_or_insert": False, "id_column": "", "donot_commit": True,
                                "data":
                                [ { 
                                    "mfd_id": mfd_id, 
                                    "id_period_type": id_period_type, 
                                    "price_dt": row[0].to_pydatetime(), 
                                    "price_open": row[1], 
                                    "price_min": row[2], 
                                    "price_max": row[3], 
                                    "price_close": row[4], 
                                    "vol": row[5],
                                    "ppredict": row[6]
                                } 
                                ]
                            }
                if not self.add_rows_from_struct(initual_data):
                    p_all_transactions_good = False
                    break
        
            if p_all_transactions_good: self._connector.commit()
            else: 
                self._connector.rollback()
                print("Была ошибка")
            return(p_all_transactions_good)

   
    def get_stocks_prices_min_max_dates(self, mfd_id, id_period_type=constants.DEFAULT_PERIOD_TYPE, dt_begin="", dt_end=""):
        '''
        Выбор и возврат информации о минимальной и максимальной дате цены на акцию, хранящихся в базе данных.
        '''
        if not self._connector:
            return(False)
        dt_begin, dt_end = self._prepare_dates(dt_begin, dt_end)   
        cur = self._connector.cursor()
        try:
            cur.execute("SELECT MIN(price_dt), MAX(price_dt) FROM STOCKS_PRICES WHERE mfd_id=? AND id_period_type=? AND price_dt BETWEEN ? AND ? AND ppredict=0",(mfd_id, id_period_type, dt_begin, dt_end))
            return(cur.fetchall())
        except:
            print("get_stocks_list: При попытке получить максммальную и минимальную даты из таблицы STOCKS_PRICES возникла ошибка.")
            return(False)


    def _prepare_dates(self, dt_begin="", dt_end=""):
        '''
        Внутреняя функция по предварительной обработке дат.
        '''
        if not dt_begin:
            dt_begin = datetime.datetime.strptime(constants.FIRST_DATETIME_IN_HISTORY, constants.DATETIME_FORMAT_SLASH)
        elif type(dt_begin)==str:
            dt_begin = datetime.datetime.strptime(dt_begin, constants.DATE_FORMAT_SLASH if len(dt_begin)==10 else constants.DATETIME_FORMAT_SLASH)
        if not dt_end:
            dt_end = datetime.datetime.now()
        elif type(dt_end)==str:
            dt_end = datetime.datetime.strptime(dt_end, constants.DATE_FORMAT_SLASH if len(dt_end)==10 else constants.DATETIME_FORMAT_SLASH)
        return (dt_begin, dt_end)
