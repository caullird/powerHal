from scholarly import scholarly

# Importation des modèles pour la création des objets
from model.entities.Institution import Institution
from model.entities.Author import Author
from model.entities.Concept import Concept
from model.relations.AuthorInstitution import AuthorInstitution
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceInstitution import SourceInstitution
from model.relations.SourceConcept import SourceConcept

class AuthorAPI():

    def __init__(self,author_name, author_forename, dataBase,sourceID):

        self.author_name = author_name
        self.author_forename = author_forename
        self.author_display_name = author_name + " " + author_forename
        self.dataBase = dataBase
        self.sourceID = sourceID

    def findAuthor(self):
        search_query = scholarly.search_author(self.author_display_name)
        try:
            self.author = scholarly.fill(next(search_query))
            return True
        except StopIteration:
            print("No author found")
            return False

    def getPublications(self):
        return self.author["publications"]

    def addAuthorInformations(self):

        dataAuthor = Author("NULL",self.author_name, self.author_forename, self.author_display_name)
        dataAuthor.setDataBase(self.dataBase)
        print(dataAuthor)
        self.AuthorID = dataAuthor.checkIfExistsOrInsert()

        dataSourceAuthor = SourceAuthor(self.AuthorID,self.sourceID,self.author["scholar_id"], {})
        dataSourceAuthor.setDataBase(self.dataBase)
        dataSourceAuthor.checkIfExistsOrInsert()

        return self.AuthorID

    def addConcepts(self):
        for concept in self.author["interests"]:
            unConcept = Concept("NULL", concept)
            unConcept.setDataBase(self.dataBase)
            idConcept = unConcept.checkIfExistsOrInsert()

            unAuthorPublicationConcept = AuthorPublicationConcept(self.AuthorID, "NULL", idConcept, 0, 100)
            unAuthorPublicationConcept.setDataBase(self.dataBase)
            unAuthorPublicationConcept.checkIfExistsOrInsert()



        
    