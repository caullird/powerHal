import requests
import json
from config.ResearchInitializer import ResearchInitializer
from model.Institution import Institution
from model.Author import Author
from model.Concept import Concept
from model.AuthorInstitution import AuthorInstitution
from model.AuthorPublicationConcept import AuthorPublicationConcept

class AuthorAPI():

    def __init__(self, research, halAPI, dataBase, filter_by):
        
        # Paramètre de recherche depuis notre solution
        self.initial_research = research
        self.intializedResearch = ResearchInitializer(research).getInitializeResearch()

        # Lien avec l'API de HAL
        self.halAPI = halAPI 
        self.filter_by = filter_by

        self.globalResponseAuthor = self.getGlobalResponseAuthor()
        self.halAuthorIDs = self.getHalAuthorIDs()  

        # Lien avec nos données sur la base mysql
        self.dataBase = dataBase

        # Ajout des informations relative à l'auteur pour
        self.idAuthor = self.addAuthorInformations()
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
            unInstitution = Institution(
                result['last_known_institution']['id'],
                result['last_known_institution']['ror'],
                result['last_known_institution']['display_name'],
                result['last_known_institution']['country_code'],
                result['last_known_institution']['type']
            )

            unInstitution.setDataBase(self.dataBase)
            idInstitution = unInstitution.checkIfExistsOrInsert()

            unAuthorInstitution = AuthorInstitution(str(self.idAuthor),str(idInstitution))
            unAuthorInstitution.setDataBase(self.dataBase)
            unAuthorInstitution.checkIfExistsOrInsert()


    # Permet de récupérer les concepts relatifs à l'auteur
    def addConceptsAuthor(self, result):
        for concept in result['x_concepts']:
            unConcept = Concept(
                concept['id'],
                concept['wikidata'],
                concept['display_name']
            )

            unConcept.setDataBase(self.dataBase)
            idConcept = unConcept.checkIfExistsOrInsert()    

            unAuthorPublicationConcept = AuthorPublicationConcept(
                str(self.idAuthor),
                "NULL",
                str(idConcept),
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
            if(result['id'] != None): resultsValues['alex_ids'].append(result['id'])

            if(result['orcid'] != None): resultsValues['orcid_ids'].append(result['orcid'])

            if(resultsValues['display_name'] == ""):
                resultsValues['display_name'] = result['display_name']
            else:
                resultsValues['names_alternatives'].append(result['display_name'])

            if(result['display_name_alternatives'] != None): resultsValues['names_alternatives'].append(result['display_name_alternatives'])
            
            if(result['works_count'] != None): resultsValues['works_count'] += result['works_count']
            
            if(result['cited_by_count'] != None): resultsValues['cited_by_count'] += result['cited_by_count']
        
        # Création du modèle et enregistrement dans la base de donnée
        unAuthor = Author(
            resultsValues['alex_ids'],
            resultsValues['orcid_ids'],
            resultsValues['display_name'],
            resultsValues['names_alternatives'],
            resultsValues['works_count'],
            resultsValues['cited_by_count']
        )

        unAuthor.setDataBase(self.dataBase)
        return unAuthor.checkIfExistsOrInsert()


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
