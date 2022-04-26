from turtle import pu
import requests
import json
from model.ConceptPublication import ConceptPublication
from model.Publication import Publication
from model.Author import Author
from model.AuthorPublication import AuthorPublication

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

            idAuthorMySQL = self.dataBase.findIdAuthorByIDAlex(id, fieldsComparable = "idsAlex_author")

            results = json.loads(requests.get(self.halAPI.getUrlAPI() + 'works?filter=' + self.filter + ':A' + id).text)
            for publication in results['results']:
                publications.append(publication) 

                # Insertion de l'ensemble des publications dans notre base de donnée
                self.addPublication(publication, idAuthorMySQL)

                # Insertion de l'ensemble des concepts dans notre base de donnée
                self.addConcepts(publication, idAuthorMySQL)

                # Insert de l'ensemble des co-auteur des publications dans notre base de donnée
                self.addCoAuthors(publication, idAuthorMySQL)

        print("INFO | " + str(len(publications)) + " publications trouvées")

    
    # Insert de l'ensemble des co-auteur des publications dans notre base de donnée
    def addCoAuthors(self,publication, idAuthorMySQL):
        pass

    # Insertion de l'ensemble des concepts dans notre base de donnée
    def addConcepts(self,publication, idAuthorMySQL):
        for concept in publication['concepts']:
            unConcept = ConceptPublication(
                concept['id'],
                concept['wikidata'],
                concept['display_name'],
                concept['level'],
                concept['score']
            )

            unConcept.setDataBase(self.dataBase)
            unConcept.checkIfExistsOrInsert()

            # Ajout de la relation entre le concept et la publication
            

    # Insertion de l'ensemble des publications dans notre base de donnée
    def addPublication(self, publication, idAuthorMySQL):
        unPublication = Publication(
            publication['id'],
            publication['doi'],
            publication['title'],
            publication['display_name'],
            publication['ids']['mag'],
            publication['type'],
            publication['publication_year'],
            publication['publication_date'],
            publication['updated_date'],
            publication['created_date']
        )  

        unPublication.setDataBase(self.dataBase)
        idPublication = unPublication.checkIfExistsOrInsert()
        
        # Ajout de la relation entre la publication et l'auteur
        unAuthorPublication = AuthorPublication(str(idAuthorMySQL),str(idPublication))
        unAuthorPublication.setDataBase(self.dataBase)
        unAuthorPublication.checkIfExistsOrInsert()