import configparser
import requests

class AlexAPI():
    def __init__(self, research):
        self.initial_research = research
        self.intializedResearch = self.initializeResearch()
        self.config = self.getConfig()
        self.urlAPI = self.getUrlAPI()

    def initializeResearch(self):
        specialChars = "!#$%^&*()" 

        result = self.initial_research

        for specialChar in specialChars:
            result = result.replace(specialChar, '')

        result = result.replace(' ', '-')

        return result.lower()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        return config

    def getUrlAPI(self):
        return self.config['OPENALEX']['URL']


    
