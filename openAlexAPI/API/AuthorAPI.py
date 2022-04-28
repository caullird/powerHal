# Importation des librairies/classes de configuration
import requests
import json

# Importation des modèles pour la création des objets
from model.Institution import Institution
from model.Author import Author
from model.Concept import Concept
from model.AuthorInstitution import AuthorInstitution
from model.AuthorPublicationConcept import AuthorPublicationConcept
from model.SourceAuthor import SourceAuthor
from model.SourceInstitution import SourceInstitution
from model.SourceConcept import SourceConcept

class AuthorAPI():

    def __init__(self, intitial_research,initializedResearch, halAPI, dataBase, sourceID, filter_by):
        
        # Paramètre de recherche depuis notre solution
        self.initial_research = intitial_research
        self.intializedResearch = initializedResearch

        # Lien avec l'API de HAL
        self.halAPI = halAPI 
        self.filter_by = filter_by

        self.globalResponseAuthor = self.getGlobalResponseAuthor()
        self.halAuthorIDs = self.getHalAuthorIDs()  

        # Lien avec nos données sur la base mysql
        self.dataBase = dataBase
        self.sourceID = sourceID

        # Ajout des informations relative à l'auteur
        self.idAuthor = self.addAuthorInformations()

        # Ajout des informatiosn externes à l'auteur
        self.addAdditionalAuthorInformations()

    # Permet de récupérer et d'ajouter les informations relative a l'auteur (en dehors de lui même)
    def addAdditionalAuthorInformations(self):
        for result in self.globalResponseAuthor['results']:
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
            'orcid_ids' : [],
            'display_name' : '',
            'names_alternatives' : [],
            'works_count' : 0,
            'cited_by_count' : 0
        }

        # Parcours de l'ensemble des données pour compiler l'ensemble des informations
        for result in self.globalResponseAuthor['results']:
            if(result['id'] != None): 
                resultsValues['alex_ids'].append(result['id'])

            if(result['orcid'] != None): 
                resultsValues['orcid_ids'].append(result['orcid'])

            resultsValues['display_name'] = self.initial_research

            if(result['display_name_alternatives'] != []): 
                resultsValues['names_alternatives'].append(result['display_name_alternatives'])
            
            if(result['works_count'] != None): 
                resultsValues['works_count'] += result['works_count']
            
            if(result['cited_by_count'] != None): 
                resultsValues['cited_by_count'] += result['cited_by_count']
        
        # Création du modèle et enregistrement dans la base de donnée
        unAuthor = Author(
            resultsValues['orcid_ids'],
            resultsValues['display_name'],
            resultsValues['names_alternatives']
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
        return json.loads(requests.get(self.halAPI.getUrlAPI() + 'authors?filter=' + self.filter_by + '.search:' + self.intializedResearch).text)


    # Permet de récupérer l'ensemble des IDS relatifs à notre paramètre
    def getHalAuthorIDs(self):
        halIDs = []
        for result in self.globalResponseAuthor['results']:
            if(len(result['ids']) > 1):
                halIDs.append(result['ids']['mag'])

        print("INFO | " + str(len(halIDs)) + " profil d'auteur valide trouvé pour le nom " + str(self.initial_research))
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
        
        
