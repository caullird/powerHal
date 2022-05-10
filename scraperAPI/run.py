from visualization.PowerCloud import PowerCloud
from visualization.PowerGraph import PowerGraph
from specific.openAlex.openAlex import openAlex
from specific.openCitation.openCitation import openCitation
from specific.googleScholar.googleScholar import googleScholar
from specific.hal.hal import hal
from specific.orcid.orcid import orcid
from config.DB import DB

class Run():

    # Initialisation de la recherche, avant de faire le pont avec l'interface web
    research = {
        "author_name" : "Salamatian",
        "author_forename" : "Kavé",
        "alternative_name" : "Kave SALAMATIAN, salamk",
        "id_connected_user" : 1,
        "id_author_as_user" : 1
    }

    # research_temp = str(research['author_forename']) + " " + str(research['author_name'])

    ## Connexion avec la base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 

    # Gestion du pont API openAlex
    openAlex(research)

    # Gestion du pont API Google Scholar
    # googleScholar(research)

    # Gestion du pont avec Open Citation
    # openCitation(research)

    # Gestion du pont avec l'API ORCID
    # orcid(dataBase,research)

    # Gestion du point avec HAL
    hal(research)

    # Creation du graph
    # PowerGraph(dataBase, research_temp)





        