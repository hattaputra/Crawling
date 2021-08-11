import os
from configparser import ConfigParser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

CF = ConfigParser()
CF.read(os.path.join(CURRENT_DIR, "config.ini"))

PROXY = CF.get('PATH', 'proxy')
PATH_FILE =