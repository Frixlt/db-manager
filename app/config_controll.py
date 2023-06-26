import configparser
from datetime import datetime

try:
    from app.data_base_functions import *
except:
    from data_base_functions import *

def create_config_file():
    final_cnfg = {}
    for i in get_column_names():
        final_cnfg[i]={}
        final_cnfg[i]["table_styles"] = ""
        final_cnfg[i]["replace_permanent"] = 0
        final_cnfg[i]["plus_permanent"] = 0
        final_cnfg[i]["replacer_default_data"] = ""
        final_cnfg[i]["data_type"] = "txt" 
    config = configparser.ConfigParser()
    for key, value in final_cnfg.items():
        section_name = key
        config[section_name] = value
    with open("app/config/config.ini", "w") as configfile:
        config.write(configfile)

def read_config():
    import configparser
    config = configparser.ConfigParser()
    config.read("app/config/config.ini")
    final_cnfg = {}
    for section_name in config.sections():
        final_cnfg[section_name] = dict(config[section_name])
    for key, value in final_cnfg.items():
        for sub_key, sub_value in value.items():
            # особые значения в конфиге
            if sub_value == "{{data}}":
                final_cnfg[key][sub_key] = datetime.now().strftime("%y-%m-%d")
    return final_cnfg

if __name__ == "__main__":
    create_config_file()