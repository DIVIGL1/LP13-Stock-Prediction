import src.constants as constants
import src.utils as utils


    
# запускается обновление исторических данных по акциям:
utils.log_print("Starting process of data updating...")
if utils.if_all_modules_exist(constants.MODULES_PARAM_GROUPS["update"]):
    import src.inet as inet
    inet.update_data()
else:
    utils.log_print("One of the modules is missing. The program is terminated.")

           
    