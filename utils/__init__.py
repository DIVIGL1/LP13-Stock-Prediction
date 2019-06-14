import os


def get_dbase_path():
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.join(basedir, "..", "Dbase")
        if not os.path.isdir(basedir): 
            os.makedirs(basedir)

        ret_path = os.path.join(basedir, "test.sqlight")
        return(ret_path)
    except:
        print("Не удалось подготовить информацию о расположении базы данных.")
        return("")

