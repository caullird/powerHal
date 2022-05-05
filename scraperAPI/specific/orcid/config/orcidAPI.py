import configparser

class orcidAPI():
    def __init__(self):
        self.config = self.getConfig()
        self.urlAPI = self.getUrlAPI()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        return config

    def getUrlAPI(self):
        return self.config['ORCID']['URL']

    

    
