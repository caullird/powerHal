# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.openCitation.config.openCitationAPI import openCitationAPI
from specific.openCitation.API.CitationAPI import CitationAPI


class openCitation():

    def __init__(self,dataBase,research, id_connected_user):
        self.dataBase = dataBase
        self.research = research
        self.id_connected_user = id_connected_user
        self.API = openCitationAPI()
        self.run()

    def run(self):
       
        initialize = ResearchInitializer(self.research)
        
        ## Permet de récupérer les informations relative à la source (id_source)
        sourceID = ResearchSource("OpenCitation", self.dataBase).getMySQLID()

        ## Récupération des informations relative à l'API

        CitationAPI(self.API, self.dataBase, self.id_connected_user, sourceID)