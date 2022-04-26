import requests
import json
from config.ResearchInitializer import ResearchInitializer
from model.Institution import Institution
from model.Concept import Concept
from model.Author import Author
from model.Publication import Publication

class PublicationAPI():

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

                unPublication = Publication(
                    article['id'],
                    article['doi'],
                    article['title'],
                    article['display_name'],
                    article['ids']['mag'],
                    article['type'],
                    article['publication_year'],
                    article['publication_date'],
                    article['updated_date'],
                    article['created_date']
                )  

                unPublication.setDataBase(self.dataBase)
                unPublication.checkIfExistsOrInsert()


        print("INFO | " + str(len(publications)) + " publications trouvées")

