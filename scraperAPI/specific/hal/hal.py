# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.hal.config.HalAPI import HalAPI
from specific.hal.API.AuthorAPI import AuthorAPI
from specific.hal.API.PublicationAPI import PublicationAPI


class hal():

    def __init__(self,dataBase,research, id_connected_user):
        self.dataBase = dataBase
        self.research = research
        self.id_connected_user = id_connected_user
        self.API = HalAPI()
        self.run()

    def run(self):
        pass