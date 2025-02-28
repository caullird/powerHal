# Importation des librairies/classes de configuration
import requests
import json
from config.ResearchInitializer import ResearchInitializer

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

    def __init__(self,research, urlAPI, dataBase, sourceID, filter_by):
        
        # Paramètre de recherche depuis notre solution
        self.research = research

        # Lien avec l'API
        self.urlAPI = urlAPI 
        self.filter_by = filter_by

        # Lien avec nos données sur la base mysql
        self.dataBase = dataBase
        self.sourceID = sourceID

        self.globalResponseAuthor = self.getGlobalResponseAuthor()
        self.mainAuthorIDS = self.getHalAuthorIDs(self.globalResponseAuthor)  

        # Ajout des informations relative à l'auteur
        self.idAuthor = self.addAuthorInformations()

        # # Ajout des informatiosn externes à l'auteur
        self.addAdditionalAuthorInformations(self.globalResponseAuthor)

        self.checkWithAlternative()
        clean_list = list(set(self.allAuthorIDS))
        self.halAuthorIDs = clean_list

    # Permet de récupérer les informations des alternatives
    def checkWithAlternative(self):
        self.allAuthorIDS = self.mainAuthorIDS
        if(self.research['alternative_name']):
            alternatives = self.research['alternative_name'].split(",")
            for alternative in alternatives:
                responseGlobal = self.getGlobalResponseAlternative(alternative)
                halAuthorIDs = self.getHalAuthorIDs(responseGlobal)
                self.addAdditionalAuthorInformations(responseGlobal)
                self.allAuthorIDS = self.allAuthorIDS + halAuthorIDs

    # Permet de récupérer et d'ajouter les informations relative a l'auteur (en dehors de lui même)
    def addAdditionalAuthorInformations(self, response):
        for result in response['results']:
            # Ajout de l'ensemble des institutions
            self.addInstitutions(result) 

            # Ajout de l'ensemble des concepts relatifs à l'auteur
            self.addConceptsAuthor(result)  


    # Permet d'ajouter l'ensemble des Institutions
    def addInstitutions(self, result):
        if(result['last_known_institution'] != None):  
            
            # Permet la création et l'ajout d'une Institution
            unInstitution = Institution(
                result['last_known_institution']['display_name'],
                result['last_known_institution']['country_code'],
                result['last_known_institution']['type']
            )

            unInstitution.setDataBase(self.dataBase)
            idInstitution = unInstitution.checkIfExistsOrInsert()
    
            # TODO : Enregistrer des informations spécifiques propre a la source
            specificInformation = {}
            
            # Permet la création du lien entre la source et une institution
            unSourceInstitution = SourceInstitution(
                idInstitution,
                self.sourceID,
                result['last_known_institution']['id'],
                specificInformation
            )
            unSourceInstitution.setDataBase(self.dataBase)
            unSourceInstitution.checkIfExistsOrInsert()

            # Permet la création du lien entre l'auteur et une institution
            unAuthorInstitution = AuthorInstitution(str(self.idAuthor),str(idInstitution))
            unAuthorInstitution.setDataBase(self.dataBase)
            unAuthorInstitution.checkIfExistsOrInsert()


    # Permet de récupérer les concepts relatifs à l'auteur
    def addConceptsAuthor(self, result):
        for concept in result['x_concepts']:
            
            # Ajout d'un concept dans la base de donnée
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

            # Permet de faire le lien entre l'auteur et le concept
            unAuthorPublicationConcept = AuthorPublicationConcept(
                self.idAuthor,
                "NULL",
                idConcept,
                concept['level'],
                concept['score']
            )
            unAuthorPublicationConcept.setDataBase(self.dataBase)
            unAuthorPublicationConcept.checkIfExistsOrInsert()


    # Permet de récupérer et d'ajouter les informations propre à l'auteur
    def addAuthorInformations(self):

        # Instantiation du tableau de résultat
        resultsValues = {
            'alex_ids' : [],
            'orcid_id' : ''
        }

        # Parcours de l'ensemble des données pour compiler l'ensemble des informations
        for result in self.globalResponseAuthor['results']:

            if(result['id'] != None): 
                resultsValues['alex_ids'].append(result['id'])

            if(result['orcid'] != None): 
                resultsValues['orcid_id'] = result['orcid'].replace("https://orcid.org/","")


        # Formation du display name en fonction de l'ordre alphabétique
        display_name = ResearchInitializer(str(self.research['author_name'] + " " + self.research['author_forename'])).getSortResearch()
        
        # Création du modèle et enregistrement dans la base de donnée
        unAuthor = Author(
            resultsValues['orcid_id'],
            self.research['author_name'],
            self.research['author_forename'],
            display_name
        )
        unAuthor.setDataBase(self.dataBase)
        AuthorID = unAuthor.checkIfExistsOrInsert()
        
        # TODO : Enregistrer des informations spécifiques propre a la source
        specificInformation = {}
    
        unSourceAuthor = SourceAuthor(AuthorID, self.sourceID, resultsValues['alex_ids'],specificInformation)
        unSourceAuthor.setDataBase(self.dataBase)
        unSourceAuthor.checkIfExistsOrInsert()
    
        return AuthorID


    # Permet de récupérer l'ensemble des informations sur l'auteur en paramètre
    def getGlobalResponseAuthor(self):
        return json.loads(requests.get(self.urlAPI + 'authors?filter=' + self.filter_by + '.search:' + str(self.research['author_name'] + " " + self.research['author_forename'])).text)


    # Permet de récupérer l'ensemble des informations sur les alternatives
    def getGlobalResponseAlternative(self, alternative):
        return json.loads(requests.get(self.urlAPI + 'authors?filter=' + self.filter_by + '.search:' + str(alternative)).text)


    # Permet de récupérer l'ensemble des IDS relatifs à notre paramètre
    def getHalAuthorIDs(self, response):
        halIDs = []
        for result in response['results']:
            if(len(result['ids']) > 1):
                halIDs.append(result['ids']['mag'])
        return halIDs


    # Permet de récupérer la liste des auteurs
    def getArrayAuthorIDs(self):
        return self.halAuthorIDs

    # Permet de récupérer l'id de l'auteur trouvé
    def getIdAuthor(self):
        return self.idAuthor
    
    # Permet de récupérer l'id de la source
    def getIdSource(self):
        self.sourceID
        
        
