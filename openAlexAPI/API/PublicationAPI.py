from turtle import pu
import requests
import json
from model.Concept import Concept
from model.Author import Author
from model.Publication import Publication
from model.AuthorPublication import AuthorPublication
from model.AuthorPublicationConcept import AuthorPublicationConcept
from config.ResearchInitializer import ResearchInitializer


class PublicationAPI():

    def __init__(self, idsAuthor, halAPI, dataBase, filter = "authorships.author.id"):
        self.idsAuthor = idsAuthor
        self.halAPI = halAPI
        self.dataBase = dataBase
        self.filter = filter
        
        self.publications = self.addPublicationInformations()


    # Permet de récupérer et d'ajouter les informations relative à la publication
    def addPublicationInformations(self):
        publications = []
        for id in self.idsAuthor:

            idAuthorMySQL = self.dataBase.findIdMySQLWithLike(id, entity = "author", fieldsComparable = "idsAlex_author")

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

            sortResearch = ResearchInitializer(author['author']['display_name']).getSortResearch()
            
            unAuthor = Author(
                author['author']['id'],
                author['author']['orcid'],
                sortResearch,
                "NULL", 0, 0
            )

            unAuthor.setDataBase(self.dataBase)
            idNewAuthor = unAuthor.checkIfExistsOrInsert()

            # Permet d'ajouter le lien entre l'auteur et la publication
            unAuthorPublication = AuthorPublication(
                str(idNewAuthor),
                str(idPublicationMySQL),
                author['author_position']
            )

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
                str(idConceptMySQL),
                str(idPublicationMySQL),
                concept['level'],
                concept['score']
            )

            unAuthorPublicationConcept.setDataBase(self.dataBase)
            unAuthorPublicationConcept.checkIfExistsOrInsert()


    # Insertion de l'ensemble des publications dans notre base de donnée
    def addPublication(self, publication, idAuthorMySQL):
        unPublication = Publication(
            publication['id'],
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
        
        # Ajout de la relation entre la publication et l'auteur
        unAuthorPublication = AuthorPublication(str(idAuthorMySQL),str(idPublicationMySQL),"first")
        unAuthorPublication.setDataBase(self.dataBase)
        unAuthorPublication.checkIfExistsOrInsert()

        return idPublicationMySQL