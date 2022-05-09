# Importation des classes pour la configuration globale au projet
from config.ResearchSource import ResearchSource
from config.DB import DB

# Importation des configurations propre à l'API
from specific.openCitation.API.CitationAPI import CitationAPI

class openCitation():

    def __init__(self,research):
        self.dataBase = DB()
        self.dataBase.setConnectedUserId(research['id_connected_user']) 
        self.id_connected_user = research['id_connected_user']
        self.run()

    def run(self):
        
        ## Permet de récupérer les informations relative à la source (id_source)
        source = ResearchSource("OpenCitation", self.dataBase)

        sourceID = source.getMySQLID()
        sourceAPIURL = source.getAPIUrl()

        ## Récupération des informations relative à l'API
        CitationAPI(sourceAPIURL, self.dataBase, self.id_connected_user, sourceID)