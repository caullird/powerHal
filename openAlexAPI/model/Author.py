import requests
import json  


class Author():

    def __init__(self, research, halAPI, dbCursor, filter_by):
        # Paramètre de recherche depuis notre solution
        self.initial_research = research
        self.intializedResearch = self.initializeResearch()

        # Lien avec l'API de HAL
        self.halAPI = halAPI 
        self.filter_by = filter_by

        self.globalResponseAuthor = self.getGlobalResponseAuthor()
        self.halAuthorIDs = self.getHalAuthorIDs()  

        # Lien avec nos données sur la base mysql
        self.dbCursor = dbCursor
        self.mySQLAuthor = self.getMySQLAuthor()


    # Permet de récupérer l'ensemble des informations sur l'auteur en paramètre
    def getGlobalResponseAuthor(self):
        return json.loads(requests.get(self.halAPI.getUrlAPI() + 'authors?filter=' + self.filter_by + '.search:' + self.intializedResearch).text)

    # Permet de récupérer l'ensemble des informations sur l'auteur de notre base mySQL en fonction de l'auteur en paramètre
    def getMySQLAuthor(self):
        return True

    # Permet de récupérer l'ensemble des IDS relatifs à notre paramètre
    def getHalAuthorIDs(self):
        halIDs = []
        for result in self.globalResponseAuthor['results']:
            halIDs.append(result['ids']['mag'])

        print("INFO | " + str(len(halIDs)) + " profil d'auteur trouvé pour le nom " + str(self.initial_research))
        return halIDs

    # Permet de mettre en forme le nom de l'auteur en paramètre
    def initializeResearch(self):
        specialChars = "!#$%^&*()" 

        result = self.initial_research

        for specialChar in specialChars:
            result = result.replace(specialChar, '')

        result = result.replace(' ', '-')

        return result.lower()