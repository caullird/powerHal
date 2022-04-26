from tokenize import String
from config.DB import DB
from config.AlexAPI import AlexAPI
from model.Author import Author

class openAlex():


    ## En attendant d'avoir le lien entre le site web et le programme python

    research = "Sorana CIMPAN"

    ## Connexion avec la base de donnée, récupération du curseur pour avoir l'accès à l'ensemble des informations 
    
    dbCursor = DB().getCursor()

    ## Récupération des id AlexAPI en fonction du nom de l'utilisateur

    API = AlexAPI()

    ## On prend les informations de l'auteurs en fonction du profil avec le plus d'interaction

    Author = Author(research, API, dbCursor, filter_by = "display_name")

    ## On compare avec nos données dans notre database 

    ## Récupération des articles en fonction des id AlexAPI

    ## Création des liens avec les autres autheurs + création des auteurs dans notre database
