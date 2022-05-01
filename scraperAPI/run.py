from specific.openAlex.openAlex import openAlex
from specific.openCitation.openCitation import openCitation

from config.DB import DB

class Run():

    id_connected_user = 1

    ## Connexion avec la base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
    dataBase = DB()
    dataBase.setConnectedUserId(id_connected_user)    
    
    # Initialisation de la recherche, avant de faire le pont avec l'interface web
    research = "Kavé SALAMATIAN"

    # Gestion du pont API openAlex
    openAlex(dataBase,research, id_connected_user)

    # Gestion du pont API openCitation
    openCitation(dataBase,research, id_connected_user)





        