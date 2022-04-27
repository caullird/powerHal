import configparser
import requests

class AlexAPI():
    def __init__(self):
        self.config = self.getConfig()
        self.urlAPI = self.getUrlAPI()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        return config

    def getUrlAPI(self):
        return "https://api.openalex.org/"
        #return self.config['OPENALEX']['URL']

    

    
