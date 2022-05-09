# Importation des classes pour la configuration globale au projet
from numpy import source
from config.DB import DB
from config.ResearchSource import ResearchSource

# # Importation des classes pour la gestion des sous-ensemble API
from specific.openAlex.API.AuthorAPI import AuthorAPI
from specific.openAlex.API.PublicationAPI import PublicationAPI

# Importation des méthodes d'analyse de données
from visualization.PowerCloud import PowerCloud
from visualization.PowerGraph import PowerGraph

class openAlex():

    def __init__(self,research):
        self.dataBase = DB()
        self.dataBase.setConnectedUserId(research['id_connected_user']) 
        self.research = research
        self.id_connected_user = research['id_connected_user']
        self.run()

    def run(self):
    
        
        ## Permet de récupérer les informations relative à la source (id_source)
        source = ResearchSource("openAlex", self.dataBase)

        sourceID = source.getMySQLID()
        sourceAPIURL = source.getAPIUrl()

        ## Importation des informations relative à l'auteur recherché
        authors = AuthorAPI(self.research, sourceAPIURL, self.dataBase, sourceID, filter_by = "display_name")

        # ## Récupération des articles en fonction des id AlexAPI & création des liens avec les autres autheurs + création des auteurs dans notre database
        publications = PublicationAPI(authors.getArrayAuthorIDs(), sourceAPIURL, self.dataBase, sourceID, authors.getIdAuthor())

        ## Différentes méthodes d'affichages de donénes
        # unWordCloud = PowerCloud(self.dataBase, "openAlex")
        # unWordCloud.generatePublicationConcept(authors.getIdAuthor())
        # unWordCloud.generatePublicationCoAuthors(authors.getIdAuthor())

        return authors.getIdAuthor()