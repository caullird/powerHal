# Importationd des fichiers de configuration
import json
import requests

# Importation des différents modèles relatifs au projet
from model.entities.Concept import Concept
from model.entities.Author import Author
from model.entities.Publication import Publication
from model.relations.AuthorPublication import AuthorPublication
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourcePublication import SourcePublication
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceConcept import SourceConcept

class PublicationAPI():
    def __init__(self, API, dataBase, sourceID = "*"):

        # Lien avec l'API 
        self.API = API  

        # Récupération des champs de recherche
        self.dataBase = dataBase
        self.sourceID = sourceID

