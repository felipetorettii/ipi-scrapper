from configparser import ConfigParser
import os

DATABASE_CONFIG_FILE_LOCAL = "database_local.ini"

def load_config(section='postgresql') -> dict:
    filename = __get_filename()
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def __get_filename() -> str:
    filename = os.environ.get('DATABASE_CONFIG_FILE', DATABASE_CONFIG_FILE_LOCAL)
    path = "./adapters/db/"
    if (filename == DATABASE_CONFIG_FILE_LOCAL):
        path = "./app/adapters/db/"
    return path+filename