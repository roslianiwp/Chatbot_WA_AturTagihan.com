import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class HedwigConfig():
    TOKEN = cfg['nexmo']['token']
    COOKIE = cfg['nexmo']['cookie']

class DevelopmentHedwig(HedwigConfig):
    URL = cfg['development']['url']
    DEBUG = True
    APP_PORT = 9000
    USERNAME = cfg['development']['username_admin']
    PASSWORD = cfg['development']['password_admin']
 
class ProductionHedwig(HedwigConfig):
    URL = cfg['production']['url']
    DEBUG = False
    APP_PORT = 5000
    USERNAME = cfg['production']['username_admin']
    PASSWORD = cfg['production']['password_admin']