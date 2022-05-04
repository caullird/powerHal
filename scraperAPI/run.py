from scraperAPI.visualization.PowerCloud import PowerCloud
from scraperAPI.visualization.PowerGraph import PowerGraph
from specific.openAlex.openAlex import openAlex
from specific.openCitation.openCitation import openCitation
from specific.googleScholar.googleScholar import googleScholar
from specific.hal.hal import hal
from config.DB import DB


class Run():

    id_connected_user = 1
    id_author_as_user = 1

    ## Connexion avec la base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
    dataBase = DB()
    dataBase.setConnectedUserId(id_connected_user)    
    
    # Initialisation de la recherche, avant de faire le pont avec l'interface web
    research = "Kavé SALAMATIAN"

    # Gestion du pont API openAlex
    # openAlex(dataBase,research, id_connected_user)

    # Gestion du pont API Google Scholar
    googleScholar(dataBase,research,5)

    # Gestion du pont avec Open Citation
    # openCitation(dataBase,research, id_connected_user)

    # Gestion du point avec HAL
    # hal(dataBase,research, id_connected_user, id_author_as_user)

    # Creation du graph
    PowerGraph(dataBase, id_connected_user)




        