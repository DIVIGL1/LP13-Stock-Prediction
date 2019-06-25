import datetime
import io
import pandas as pd
import requests
import time

import db
import constants
import utils

class Inet_connector():
    '''
        This class performs connection through API to Internet resource
        and gives functionality to download information about stocks's prices.
    '''
    def __init__(self, str_api_url, dict_api_params):
        self.api_url = str_api_url
        self.api_params = dict_api_params

    def get_stocks_prices_2df(self, mfd_id, id_period_type=constants.DEFAULT_PERIOD_TYPE, date_begin="", date_end=""):
        '''
            This method downloads information about stocks's prices for period between <date_begin> and <date_end>.
            If period is bigger then 100 days it's divided into groups of 100 days.
            The result is returned in DataFrame format.
        '''
        date_begin, date_end = self._prepare_dates(date_begin, date_end)

        self.api_params["Tickers"] = str(mfd_id)
        self.api_params["Period"] = str(id_period_type)

        # Загружаем партиями по 100 дней, так как ресурс не даёт выгружать большие файлы.
        # В date_begin и date_end у на Даты, а не ДатаВремя
        first_load_date = date_begin
        continue_load_data = True
        while continue_load_data:
            last_load_date = first_load_date + datetime.timedelta(days=100)
            if last_load_date>date_end:
                continue_load_data = False
                last_load_date = date_end
            # ------------------------------
            self.api_params["StartDate"] = datetime.datetime.strftime(first_load_date, constants.API_PARAMS_DATE_FORMAT)
            self.api_params["EndDate"] = datetime.datetime.strftime(last_load_date, constants.API_PARAMS_DATE_FORMAT)
            orequest = requests.get(self.api_params, params=self.api_params)
            file_in_memory = io.StringIO(orequest.text)
            df = pd.read_csv(file_in_memory, sep=";")

            df = utils.prepare_df(df)
            time.sleep(0.5)               # Задержка в секундах.
            # ------------------------------
            if first_load_date==date_begin:
                # Это первый кусочек данных из всех.
                # К нему будем присоединять остальные.
                ret_df = df
            else:
                ret_df = pd.concat([ret_df, df], axis=0, ignore_index=True)
                
            first_load_date = last_load_date + datetime.timedelta(days=1)

        return(ret_df)
    
    def update_data(self):
        otimer = utils.Timer("Get started loading all stocks prices:")
        dh = db.Data_handler()
        stocks_list = dh.get_stocks_list()
        for one_stoks in stocks_list:
            print("\nLoading prices for {}, {}".format(one_stoks[0], one_stoks[2]))
            self.load_stock_prises_from_inet(mfd_id=one_stoks[1])
        otimer.show()

    def load_stock_prises_from_inet(self, mfd_id, id_period_type=constants.DEFAULT_PERIOD_TYPE, date_begin="", date_end=""):

        date_begin, date_end = self._prepare_dates(date_begin, date_end)

        # так как нам нужно найти последнюю дату в БД,
        # а там хратися DateTime, а у нас в переменной Date
        # то преобразуем дату в соотвествии с примером:
        # 20/01/2019 --> 20/01/2019 23:59:59
        dt_end = datetime.datetime(date_end.year, date_end.month, date_end.day) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        # При этом dt_begin будет типа 01/01/2019 00:00:00
        dt_begin = datetime.datetime(date_begin.year, date_begin.month, date_begin.day)

        dh = db.Data_handler()
        ret_value = dh.get_stocks_prices_min_max_dates( 
                                                        mfd_id=mfd_id, 
                                                        id_period_type=id_period_type, 
                                                        dt_begin=dt_begin, 
                                                        dt_end=dt_end
                                                      )
        if ret_value==[(None, None)]:
            # В БД нет данных для данной акции и для данного типа периода.
            date_max = date_begin - datetime.timedelta(days=1)
            date_min = date_max
        else:
            date_min = datetime.datetime.strptime(ret_value[0][0], constants.DATETIME_FORMAT_IN_DB).date()
            date_max = datetime.datetime.strptime(ret_value[0][1], constants.DATETIME_FORMAT_IN_DB).date()

        if date_begin<date_min:
            df = self.get_stocks_prices_2df( 
                                            mfd_id=mfd_id, 
                                            id_period_type=id_period_type, 
                                            date_begin=date_begin, 
                                            date_end=date_min-datetime.timedelta(days=1)
                                            )
            if df.shape[0]!=0:
                print("Подгружаем данные за период с {} по {}.".format(date_begin, date_min-datetime.timedelta(days=1)))
                dh.load_stock_prises_from_df2db(mfd_id=mfd_id, id_period_type=id_period_type, df=df)

        if date_max<date_end:
            df = self.get_stocks_prices_2df( 
                                                        mfd_id=mfd_id, 
                                                        id_period_type=id_period_type, 
                                                        date_begin=date_max + datetime.timedelta(days=1), 
                                                        date_end=date_end
                                                     )
            if df.shape[0]!=0:
                print("Подгружаем данные за период с {} по {}.".format(date_max + datetime.timedelta(days=1), date_end))
                dh.load_stock_prises_from_df2db(mfd_id=mfd_id, id_period_type=id_period_type, df=df)


    def _prepare_dates(self, date_begin="", date_end=""):
        if not date_begin:
            date_begin = datetime.datetime.strptime(constants.FIRST_DAY_IN_HISTORY, constants.DATE_FORMAT_SLASH).date()
        elif type(date_begin)==str:
            date_begin = datetime.datetime.strptime(date_begin, constants.DATE_FORMAT_SLASH).date()

        if not date_end:
            date_end = datetime.datetime.now().date()
        elif type(date_end)==str:
            date_end = datetime.datetime.strptime(date_end, constants.DATE_FORMAT_SLASH).date()

        return(date_begin, date_end)


def update_data():
    ic = Inet_connector(constants.API_URL, constants.API_PARAMS)
    ic.update_data()
