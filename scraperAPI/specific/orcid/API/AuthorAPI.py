# Importationd des fichiers de configuration
import json
import requests
import wget

# Importation des différents modèles relatifs au projet
from model.entities.Concept import Concept
from model.entities.Author import Author
from model.entities.Publication import Publication
from model.relations.AuthorPublication import AuthorPublication
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourcePublication import SourcePublication
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceConcept import SourceConcept

class AuthorAPI():
    def __init__(self, API, dataBase, sourceID = "*"):

        # Lien avec l'API 
        self.API = API  

        # Récupération des champs de recherche
        self.dataBase = dataBase
        self.sourceID = sourceID

        self.getORCIDInformation()

    def getORCIDInformation(self):
        
        # Récupération de l'ensemble des auteurs 

        authors = self.dataBase.getAll("Author")

        for author in authors:
            if(author[1] == ""):

                # Récupération de l'information sur l'auteur
                self.addORCID(author)

            else : 
                # Récupération des informations complémentairesd
                pass
        

    def addORCID(self, author):
        try:
            request = "https://pub.orcid.org/v3.0/csv-search/?q=given-names:" + author[3].replace(' ','') + "+&+family-name:" + author[2].replace(' ','')
            response = wget.download(request, "poubelle/result - " + author[3].replace(' ','') + " - " + author[2].replace(' ','') +".csv")
        except :
            print("error")
