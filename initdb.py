import src.constants as constants
import src.utils as utils

# запускается блок по созданию и инициализации базы данных:
utils.log_print("Starting initialisation of DBase...")
if utils.if_all_modules_exist(constants.MODULES_PARAM_GROUPS["initdb"]):
    import src.db as db
    db.Data_handler()           
else:
    utils.log_print("One of the modules is missing. The program is terminated.")
