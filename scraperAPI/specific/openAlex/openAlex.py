# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.ResearchSource import ResearchSource

# Importation des configurations propre à l'API
from specific.openAlex.config.AlexAPI import AlexAPI

# # Importation des classes pour la gestion des sous-ensemble API
from specific.openAlex.API.AuthorAPI import AuthorAPI
from specific.openAlex.API.PublicationAPI import PublicationAPI

# Importation des méthodes d'analyse de données
from visualization.PowerCloud import PowerCloud
from visualization.PowerGraph import PowerGraph

class openAlex():

    def __init__(self,dataBase,research, id_connected_user):
        self.dataBase = dataBase
        
        self.research = research
        self.id_connected_user = id_connected_user
        self.run()

    def run(self):
       
        initialize = ResearchInitializer(self.research)
        
        ## Permet de récupérer les informations relative à la source (id_source)
        sourceID = ResearchSource("openAlex", self.dataBase).getMySQLID()

        ## Récupération des informations relative à l'API
        API = AlexAPI()

        ## Importation des informations relative à l'auteur recherché
        authors = AuthorAPI(initialize.getSortResearch(), initialize.getPrepareResearch(), API, self.dataBase, sourceID, filter_by = "display_name")

        ## Récupération des articles en fonction des id AlexAPI & création des liens avec les autres autheurs + création des auteurs dans notre database
        publications = PublicationAPI(authors.getArrayAuthorIDs(), API, self.dataBase, sourceID, authors.getIdAuthor())

        ## Différentes méthodes d'affichages de donénes
        unWordCloud = PowerCloud(self.dataBase, "openAlex")
        unWordCloud.generatePublicationConcept(authors.getIdAuthor())
        unWordCloud.generatePublicationCoAuthors(authors.getIdAuthor())

        return authors.getIdAuthor()