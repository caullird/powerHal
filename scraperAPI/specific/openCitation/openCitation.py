# Importation des classes pour la configuration globale au projet
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.openCitation.config.openCitationAPI import openCitationAPI
from specific.openCitation.API.CitationAPI import CitationAPI


class openCitation():

    def __init__(self,dataBase,research):
        self.dataBase = dataBase
        self.id_connected_user = research['id_connected_user']
        self.API = openCitationAPI()
        self.run()

    def run(self):
        
        ## Permet de récupérer les informations relative à la source (id_source)
        sourceID = ResearchSource("OpenCitation", self.dataBase).getMySQLID()

        ## Récupération des informations relative à l'API
        CitationAPI(self.API, self.dataBase, self.id_connected_user, sourceID)