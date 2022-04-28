# Importation des librairies/classes de configuration
import requests
import json
from config.ResearchInitializer import ResearchInitializer

# Importation des modèles pour la création des objets
from model.Concept import Concept
from model.Author import Author
from model.Publication import Publication
from model.AuthorPublication import AuthorPublication
from model.AuthorPublicationConcept import AuthorPublicationConcept
from model.SourcePublication import SourcePublication
from model.SourceAuthor import SourceAuthor
from model.SourceConcept import SourceConcept

class PublicationAPI():

    def __init__(self, idsAuthor, halAPI, dataBase, sourceID, authorID):
        self.idsAuthor = idsAuthor
        self.halAPI = halAPI
        self.dataBase = dataBase
        self.sourceID = sourceID
        self.authorID = authorID
        
        self.publications = self.addPublicationInformations()


    # Permet de récupérer et d'ajouter les informations relative à la publication
    def addPublicationInformations(self):
        publications = []
        for id in self.idsAuthor:

            idAuthorMySQL = self.authorID

            results = json.loads(requests.get(self.halAPI.getUrlAPI() + 'works?filter=authorships.author.id:A' + id).text)
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

            # Permet d'uniformiser le nom de l'auteur
            display_name = ResearchInitializer(author['author']['display_name']).getSortResearch()
            
            display_name_alternatives = []
            orcid_id = []

            if author['author']['orcid'] != None:
                orcid_id.append(author['author']['orcid'])

            # Permet d'enregistrer le co-auteur en tant que auteur dans notre BDD
            unAuthor = Author(orcid_id,display_name,display_name_alternatives)
            unAuthor.setDataBase(self.dataBase)
            idNewAuthor = unAuthor.checkIfExistsOrInsert()
            
            # TODO : Enregistrer des informations spécifiques propre a la source
            specificInformation = {}
            
            # Permet d'ajouter le lien entre l'auteur et la source
            unSourceAuthor = SourceAuthor(idNewAuthor, self.sourceID, author['author']['id'], specificInformation)
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
                concept['wikidata'],
                concept['display_name']
            )
            unConcept.setDataBase(self.dataBase)
            idConcept = unConcept.checkIfExistsOrInsert()
            
            # TODO : Enregistrer des informations spécifiques propre a la source
            specificInformation = {}
            
            # Permet de faire le lien entre la source et le concept              
            unSourceConcept = SourceConcept(idConcept,self.sourceID,concept['id'], specificInformation)
            unSourceConcept.setDataBase(self.dataBase)
            unSourceConcept.checkIfExistsOrInsert()

            # Ajout de la relation entre le concept et la publication
            unAuthorPublicationConcept = AuthorPublicationConcept(
                "NULL",
                idConcept,
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
            publication['created_date'],
            self.sourceID
        )  

        unPublication.setDataBase(self.dataBase)
        idPublicationMySQL = unPublication.checkIfExistsOrInsert()
        
        # TODO : Enregistrer des informations spécifiques propre a la source
        specificInformation = {}
        
        # Aujout de la relation entre la publication et la source 
        unSourcePublication = SourcePublication(idPublicationMySQL,self.sourceID,publication['id'], specificInformation)
        unSourcePublication.setDataBase(self.dataBase)
        unSourcePublication.checkIfExistsOrInsert()
        
        # Ajout de la relation entre la publication et l'auteur
        unAuthorPublication = AuthorPublication(idAuthorMySQL,idPublicationMySQL,"first")
        unAuthorPublication.setDataBase(self.dataBase)
        unAuthorPublication.checkIfExistsOrInsert()

        return idPublicationMySQL