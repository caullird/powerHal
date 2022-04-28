from openAlex import openAlex

class Run():
    
    # Initialisation de la recherche, avant de faire le pont avec l'interface web
    research = "Kavé SALAMATIAN"

    # Importation des données depuis OpenAlex et récupération de l'auteur importé
    idAuthor = openAlex(research)


        