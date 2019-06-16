import datetime
import os
import time

def get_dbase_path():
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.join(basedir, "DBase")
        if not os.path.isdir(basedir): 
            os.makedirs(basedir)

        ret_path = os.path.join(basedir, "test.sqlight")
        return(ret_path)
    except:
        print("Не удалось подготовить информацию о расположении базы данных.")
        return("")

def prepare_df(df):
    columns_list = df.columns

    if not (
        ("<DATE>" in columns_list) and
        ("<TIME>" in columns_list) and
        ("<CLOSE>" in columns_list) and
        ("<VOL>" in columns_list)
            ):
        print("prepare_df: Указанный файл не содержит нужных столбцов.")
        return(False)
    if not ("<OPEN>" in columns_list): df["<OPEN>"] = df["<CLOSE>"]
    if not ("<HIGH>" in columns_list): df["<HIGH>"] = df["<CLOSE>"]
    if not ("<LOW>" in columns_list): df["<LOW>"] = df["<CLOSE>"]
    
    if not df.shape[0]==0:
        df["<DATE>"] = df["<DATE>"].astype(str)
        df["<TIME>"] = df["<TIME>"].apply(lambda x: '{0:06}'.format(x))
        df["<DT>"] = df[["<DATE>", "<TIME>"]].apply(lambda dt: datetime.datetime.strptime(dt[0]+" "+dt[1], "%Y%m%d %H%M%S"), axis=1)
    else:
        df["<DT>"] = df["<DATE>"]
    # Вернём только нужные столбцы и в нужном порядке.
    return(df[["<DT>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<VOL>"]])

class Timer():
    def __init__(self, timer_name=""):
        self.timer_name = timer_name
        self.start_position_of_timer = time.time()
        duration_in_seconds = int(time.time() - self.start_position_of_timer)
        self.print_text(duration_in_seconds)

    def show(self):
        # Функция для отображения времени
        duration_in_seconds = int(time.time() - self.start_position_of_timer)
        self.print_text(duration_in_seconds)

    def print_text(self, duration_in_seconds):
        print_timer_str = "--- {0:0>2}:{1:0>2} ---".format(duration_in_seconds // 60, duration_in_seconds % 60)
        print_spaces = " " * 5
        print_separator_line = "-" * (len(self.timer_name) + len(print_spaces)) + "-" * len(print_timer_str)

        print_timer_str = self.timer_name + print_spaces + print_timer_str

        print(print_separator_line)
        print(print_timer_str)
        print(print_separator_line)


def d2dt(date):
    return(datetime.datetime(date.year, date.month, date.day))
def last_second_of_date(date):
    return(d2dt(date) + datetime.timedelta(days=1) - datetime.timedelta(seconds=1))

def if_module_exist(module_name):
    module_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), module_name + ".py")
    return(os.path.exists(module_path))

def log_print(text):
    if not if_module_exist("logging_prosses"):
        print(text)
    else:
        import logging_prosses
        logging_prosses.log_print(text)
