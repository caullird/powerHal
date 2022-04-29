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

class CitationAPI():
    def __init__(self, API, dataBase, authorID, sourceID):

        # Lien avec l'API 
        self.API = API  

        # Récupération des champs de recherche
        self.dataBase = dataBase
        self.authorID = authorID
        self.sourceID = sourceID

        # Application des différentes méthodes
        self.defValidePublication()

    def defValidePublication(self):
        getPublications = self.dataBase.getFieldsWithId(self.authorID,"Publication",self.authorID,"*", quantity = "many")

        for publication  in getPublications:
            idPublication = publication[0]
            idDoi = publication[1]
            if idDoi not in ["","[]","{}","()","NULL","None"]:
                unSourcePublication = SourcePublication(idPublication,self.sourceID,"","{}")
                unSourcePublication.setDataBase(self.dataBase)
                unSourcePublication.checkIfExistsOrInsert()

                citation_count = self.getAPIResponse(idDoi, field = "citation-count")
                reference_count = self.getAPIResponse(idDoi, field = "reference-count")

                self.dataBase.updateOneField(id = idPublication, table = "Publication", field = "citation_count", value = citation_count[0]['count'])
                self.dataBase.updateOneField(id = idPublication, table = "Publication", field = "reference_count", value = reference_count[0]['count'])


    def getAPIResponse(self, doiId, field):
        return json.loads(requests.get(self.API.getUrlAPI() + field + '/' + str(doiId) ).text)


