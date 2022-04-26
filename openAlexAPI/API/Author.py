import requests
import json
from config.ResearchInitializer import ResearchInitializer
from model.Institution import Institution

class Author():

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
        self.institutions = self.getInstitutions()

    # Permet de récupérer et d'ajouter les institution relative a l'auteur
    def getInstitutions(self):
        for result in self.globalResponseAuthor['results']:
            if(result['last_known_institution'] != None):
                    
                unInstitution = Institution(
                    result['last_known_institution']['id'],
                    result['last_known_institution']['ror'],
                    result['last_known_institution']['display_name'],
                    result['last_known_institution']['country_code'],
                    result['last_known_institution']['type']
                )

                unInstitution.setDataBase(self.dataBase)
                unInstitution.checkIfExists()

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
