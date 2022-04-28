# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchInitializer import ResearchInitializer
from config.Source import Source

# Importation des configurations propre à AlexAPI
from specific.openAlex.config.AlexAPI import AlexAPI

# # Importation des classes pour la gestion des sous-ensemble API
from specific.openAlex.API.AuthorAPI import AuthorAPI
from specific.openAlex.API.PublicationAPI import PublicationAPI

# Importation des méthodes d'analyse de données
from analyze.PowerCloud import PowerCloud
from analyze.PowerGraph import PowerGraph

class openAlex():

    def __init__(self,research):
        self.research = research
        self.run()

    def run(self):
       
        initialize = ResearchInitializer(self.research)
        
        ## Connexion avec laclea base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
        dataBase = DB()
        
        ## Permet de récupérer les informations relative à la source (id_source)
        sourceID = Source("openAlex", dataBase).getMySQLID()

        ## Récupération des informations relative à l'API
        API = AlexAPI()

        ## Importation des informations relative à l'auteur recherché
        authors = AuthorAPI(initialize.getSortResearch(), initialize.getPrepareResearch(), API, dataBase, sourceID, filter_by = "display_name")

        ## Récupération des articles en fonction des id AlexAPI & création des liens avec les autres autheurs + création des auteurs dans notre database
        publications = PublicationAPI(authors.getArrayAuthorIDs(), API, dataBase, sourceID, authors.getIdAuthor())

        ## Différentes méthodes d'affichages de donénes
        unWordCloud = PowerCloud(dataBase, "openAlex")
        unWordCloud.generatePublicationConcept(authors.getIdAuthor())
        unWordCloud.generatePublicationCoAuthors(authors.getIdAuthor())

        # Fermeture de la connexion avec la base de donnée
        dataBase.close()