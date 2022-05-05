# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.orcid.config.orcidAPI import orcidAPI
from specific.orcid.API.AuthorAPI import AuthorAPI


class orcid():

    def __init__(self,dataBase, research):
        self.dataBase = dataBase
        self.id_connected_user = research['id_connected_user']
        self.API = orcidAPI()
        self.run()

    def run(self):
        AuthorAPI(self.API, self.dataBase)


