from scholarly import scholarly

# Importation des modèles pour la création des objets
from model.entities.Concept import Concept
from model.entities.Author import Author
from model.entities.Publication import Publication
from model.entities.Document import Document
from model.relations.AuthorPublication import AuthorPublication
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourcePublication import SourcePublication
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceConcept import SourceConcept


class PublicationAPI:

    def __init__(self, publications, database, authorID, sourceID):
        self.publications = publications
        self.dataBase = database
        self.authorID = authorID
        self.sourceID = sourceID

    def addPublications(self, max):
        for publication in self.publications[:max]:
            self.checkIfExistOrAdd(publication)

    def checkIfExistOrAdd(self, publication):
        tempPublication = Publication("NULL",publication["bib"]["title"],"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL")
        if self.dataBase.checkIfExists(tempPublication, fieldsComparable = ["title"]):
            return True
        else:
            filledPublication = scholarly.fill(publication)
            unePublication = Publication("NULL", filledPublication["bib"]["title"],filledPublication["bib"]["title"],"NULL", filledPublication["bib"]["pub_year"],"NULL","NULL","NULL",self.sourceID,filledPublication["num_citations"])
            unePublication.setDataBase(self.dataBase)
            self.publicationID = unePublication.checkIfExistsOrInsert()

            unSourcePublication = SourcePublication(self.publicationID,self.sourceID,filledPublication["author_pub_id"], "NULL")
            unSourcePublication.setDataBase(self.dataBase)
            unSourcePublication.checkIfExistsOrInsert()

            unAuthorPublication = AuthorPublication(self.authorID,self.publicationID,"first")
            unAuthorPublication.setDataBase(self.dataBase)
            unAuthorPublication.checkIfExistsOrInsert()

            self.addCoAuthors(filledPublication["bib"]["author"])


    def addCoAuthors(self,coAuthors):
        authors = coAuthors.split(" and ")
        print(authors)
        for author in authors:
            unAuthor = Author("NULL",author,"NULL")
            unAuthor.setDataBase(self.dataBase)
            authorID = unAuthor.checkIfExistsOrInsert()
            
            print(author)
            
            unAuthorPublication = AuthorPublication(authorID,self.publicationID,"first")
            unAuthorPublication.setDataBase(self.dataBase)
            unAuthorPublication.checkIfExistsOrInsert()


        