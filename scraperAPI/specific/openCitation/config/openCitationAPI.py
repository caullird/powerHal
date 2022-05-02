import configparser

class openCitationAPI():
    def __init__(self):
        self.config = self.getConfig()
        self.urlAPI = self.getUrlAPI()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        return config

    def getUrlAPI(self):
        #return self.config['OPENCITATION']['URL']
        return "https://opencitations.net/index/api/v1/"

    

    
