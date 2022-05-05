# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.orcid.config.orcidAPI import orcidAPI
from specific.orcid.API.PublicationAPI import PublicationAPI


class orcid():

    def __init__(self,dataBase,research, id_connected_user):
        self.dataBase = dataBase
        self.research = research
        self.id_connected_user = id_connected_user
        self.API = orcidAPI()
        self.run()

    def run(self):
        
        PublicationAPI(self.API, self.dataBase, self.id_connected_user)


