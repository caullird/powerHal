from specific.openAlex.openAlex import openAlex

from config.DB import DB

class Run():

    id_connected_user = 1

    ## Connexion avec la base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
    dataBase = DB()
    
    # Initialisation de la recherche, avant de faire le pont avec l'interface web
    research = "Kavé SALAMATIAN"

    # Importation des données depuis OpenAlex et récupération de l'auteur importé
    idAuthor = openAlex(dataBase, research, id_connected_user)


        