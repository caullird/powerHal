import requests
import json
from config.ResearchInitializer import ResearchInitializer
from model.Institution import Institution
from model.Concept import Concept
from model.Author import Author

class Publication():

    def __init__(self, idsAuthor, halAPI, dataBase, filter = "authorships.author.id"):
        self.idsAuthor = idsAuthor
        self.halAPI = halAPI
        self.dataBase = dataBase
        self.filter = filter
        
        self.publications = self.getPublications()


    def getPublications(self):
        publications = []
        for id in self.idsAuthor:
            results = json.loads(requests.get(self.halAPI.getUrlAPI() + 'works?filter=' + self.filter + ':A' + id).text)
            for article in results['results']:
                publications.append(article)

        print("INFO | " + str(len(publications)) + " publications trouvées")
    ##https://api.openalex.org/works?filter=authorships.author.id:A166706192