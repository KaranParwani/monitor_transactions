import configparser
import os

config = configparser.ConfigParser()

config_file_path = os.path.join(os.getcwd(), 'config\config.ini') 
config.read(config_file_path)

HOST = config['database'].get('host')
PORT = config['database'].getint('port')
auto_reload = config['database'].getboolean('auto_reload')
API_KEY = config['acc_api_key'].get('api_key')