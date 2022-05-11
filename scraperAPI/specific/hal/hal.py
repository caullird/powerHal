# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.hal.API.PublicationAPI import PublicationAPI

class hal:

    def __init__(self,research):
        self.dataBase = DB()
        self.dataBase.setConnectedUserId(research['id_connected_user']) 

        self.research = research
        self.run()

    def run(self):
        
        ## Permet de récupérer les informations relative à la source (id_source)
        source = ResearchSource("hal", self.dataBase)

        sourceID = source.getMySQLID()
        sourceAPIURL = source.getAPIUrl()
        
        PublicationAPI(self.dataBase, self.research, sourceAPIURL, sourceID)