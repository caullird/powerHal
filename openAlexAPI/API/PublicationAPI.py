from turtle import pu
import requests
import json
from model.Concept import Concept
from model.Author import Author
from model.Publication import Publication
from model.AuthorPublication import AuthorPublication
from model.AuthorPublicationConcept import AuthorPublicationConcept
from model.SourcePublication import SourcePublication
from model.SourceAuthor import SourceAuthor
from config.ResearchInitializer import ResearchInitializer

class PublicationAPI():

    def __init__(self, idsAuthor, halAPI, dataBase, sourceID, authorID, filter = "authorships.author.id"):
        self.idsAuthor = idsAuthor
        self.halAPI = halAPI
        self.dataBase = dataBase
        self.filter = filter
        self.sourceID = sourceID
        self.authorID = authorID
        
        self.publications = self.addPublicationInformations()


    # Permet de récupérer et d'ajouter les informations relative à la publication
    def addPublicationInformations(self):
        publications = []
        for id in self.idsAuthor:

            #idAuthorMySQL = self.dataBase.findIdMySQLWithLike(id, entity = "author", fieldsComparable = "display_name")
            idAuthorMySQL = self.authorID

            results = json.loads(requests.get(self.halAPI.getUrlAPI() + 'works?filter=' + self.filter + ':A' + id).text)
            for publication in results['results']:
                publications.append(publication) 

                # Insertion de l'ensemble des publications dans notre base de donnée
                idPublicationMySQL = self.addPublication(publication, idAuthorMySQL)

                # Insertion de l'ensemble des concepts dans notre base de donnée
                self.addConcepts(publication, idAuthorMySQL, idPublicationMySQL)

                # Insert de l'ensemble des co-auteur des publications dans notre base de donnée
                self.addCoAuthors(publication, idPublicationMySQL)

        print("INFO | " + str(len(publications)) + " publications trouvées")

    
    # Insert de l'ensemble des co-auteur des publications dans notre base de donnée
    def addCoAuthors(self,publication, idPublicationMySQL):
        for author in publication['authorships']:

            display_name = ResearchInitializer(author['author']['display_name']).getSortResearch()
            
            unAuthor = Author(
                author['author']['orcid'],
                display_name,
                "NULL"
            )
            unAuthor.setDataBase(self.dataBase)
            idNewAuthor = unAuthor.checkIfExistsOrInsert()
            
            unSourceAuthor = SourceAuthor(idNewAuthor, self.sourceID, author['author']['id'])
            unSourceAuthor.setDataBase(self.dataBase)
            unSourceAuthor.checkIfExistsOrInsert()

            # Permet d'ajouter le lien entre l'auteur et la publication
            unAuthorPublication = AuthorPublication(idNewAuthor, idPublicationMySQL, author['author_position'])
            unAuthorPublication.setDataBase(self.dataBase)
            unAuthorPublication.checkIfExistsOrInsert()


    # Insertion de l'ensemble des concepts dans notre base de donnée
    def addConcepts(self,publication, idAuthorMySQL, idPublicationMySQL):
        for concept in publication['concepts']:

            unConcept = Concept(
                concept['id'],
                concept['wikidata'],
                concept['display_name']
            )

            unConcept.setDataBase(self.dataBase)
            idConceptMySQL = unConcept.checkIfExistsOrInsert()

            # Ajout de la relation entre le concept et la publication

            unAuthorPublicationConcept = AuthorPublicationConcept(
                "NULL",
                idConceptMySQL,
                idPublicationMySQL,
                concept['level'],
                concept['score']
            )

            unAuthorPublicationConcept.setDataBase(self.dataBase)
            unAuthorPublicationConcept.checkIfExistsOrInsert()


    # Insertion de l'ensemble des publications dans notre base de donnée
    def addPublication(self, publication, idAuthorMySQL):
        unPublication = Publication(
            publication['doi'],
            publication['title'],
            publication['display_name'],
            publication['type'],
            publication['publication_year'],
            publication['publication_date'],
            publication['updated_date'],
            publication['created_date']
        )  

        unPublication.setDataBase(self.dataBase)
        idPublicationMySQL = unPublication.checkIfExistsOrInsert()
        
        # Aujout de la relation entre la publication et la source 
        unSourcePublication = SourcePublication(idPublicationMySQL,self.sourceID,publication['id'])
        unSourcePublication.setDataBase(self.dataBase)
        unSourcePublication.checkIfExistsOrInsert()
        
        # Ajout de la relation entre la publication et l'auteur
        unAuthorPublication = AuthorPublication(idAuthorMySQL,idPublicationMySQL,"first")
        unAuthorPublication.setDataBase(self.dataBase)
        unAuthorPublication.checkIfExistsOrInsert()

        return idPublicationMySQL