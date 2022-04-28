# Importation des classes pour la configuration
from config.DB import DB
from config.AlexAPI import AlexAPI
from config.ResearchInitializer import ResearchInitializer
from config.Source import Source

# Importation des classes pour la gestion des sous-ensemble API
from API.AuthorAPI import AuthorAPI
from API.PublicationAPI import PublicationAPI

class openAlex():
    
    # Permet d'activer ou non le mode DEBUG 
    debug = True
    
    ## En attendant d'avoir le lien entre le site web et le programme python
    research = "Cave Jonathan"
    
    initialize = ResearchInitializer(research)
    
    ## Connexion avec laclea base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
    dataBase = DB(debug)
    
    ## Permet de récupérer les informations relative à la source (id_source)
    sourceID = Source("openAlex", dataBase).getMySQLID()

    ## Récupération des informations relative à l'API
    API = AlexAPI()

    ## Importation des informations relative à l'auteur recherché
    authors = AuthorAPI(initialize.getSortResearch(), initialize.getPrepareResearch(), API, dataBase, sourceID, filter_by = "display_name")

    ## Récupération des articles en fonction des id AlexAPI & création des liens avec les autres autheurs + création des auteurs dans notre database
    publications = PublicationAPI(authors.getArrayAuthorIDs(), API, dataBase, sourceID, authors.getIdAuthor())

    # Fermeture de la connexion avec la base de donnée
    dataBase.close()