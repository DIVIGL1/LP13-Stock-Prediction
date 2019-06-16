# -*- coding: utf-8 -*-
import sys
import argparse

import utils

def createParser():
    # Используем библиотеку "argparse" для разбора переданных параметров.
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default='initdb')
    return(parser)

def do_command():
    # При старте программы получаем и анализируем переданные парамерты:
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    # Далее в зависимости от полученной команды запускаем соответствующую ветку кода:
    if namespace.name=="initdb":
        # запускается блок по созданию и инициализации базы данных:
        utils.log_print("Starting initialisation of DBase...")
        if utils.if_module_exist("bd") and utils.if_module_exist("constants") and utils.if_module_exist("utils"):
            utils.log_print("Starting process of DBase initialisation...")
            import db
            dh.Data_handler()
            return(True)
        else:
            utils.log_print("One of the modules is missing. The program is terminated.")
            return(False)
    elif namespace.name=="start":
        # запускается сервер обеспечивающий взаимодействие с пользователем:
        utils.log_print("Starting server...")
        if \
            utils.if_module_exist("bd") and \
            utils.if_module_exist("prediction") and \
            utils.if_module_exist("server") and \
            utils.if_module_exist("constants") and \
            utils.if_module_exist("utils") and \
            utils.if_module_exist("inet"):
                
            import server
            server.start_server()
            return(True)
        else:
            utils.log_print("One of the modules is missing. The program is terminated.")
            return(False)
    elif namespace.name=="update":
        # запускается обновление исторических данных по акциям:
        utils.log_print("Starting process of data updating...")
        if \
            utils.if_module_exist("bd") and \
            utils.if_module_exist("constants") and \
            utils.if_module_exist("utils") and \
            utils.if_module_exist("inet"):
                
            import inet
            inet.update_data()
            return(True)
        else:
            utils.log_print("One of the modules is missing. The program is terminated.")
            return(False)
    elif namespace.name=="predict":
        # запускается функционал по расчету новых предсказаний и удалению старых:
        utils.log_print("Starting process of behavior predicting...")
        if \
            utils.if_module_exist("bd") and \
            utils.if_module_exist("prediction") and \
            utils.if_module_exist("constants") and \
            utils.if_module_exist("utils") and \
            utils.if_module_exist("ui") and \
            utils.if_module_exist("inet"):
                
            import prediction
            prediction.start_prediction()
            return(True)
        else:
            return(False)
    else:
        utils.log_print("Unknown argument: {}.".format(namespace.name))


do_command()
