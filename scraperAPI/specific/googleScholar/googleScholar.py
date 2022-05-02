from specific.googleScholar.API.AuthorAPI import AuthorAPI
from specific.googleScholar.API.PublicationAPI import PublicationAPI

from config.ResearchSource import ResearchSource

class googleScholar():

    def __init__(self,dataBase,research, id_connected_user):
        self.dataBase = dataBase
        self.research = research
        self.id_connected_user = id_connected_user
        self.sourceID = ResearchSource("googleScholar", self.dataBase).getMySQLID()
        self.run()

    def run(self):

        author = AuthorAPI(self.research, self.dataBase,self.sourceID)
        if author.findAuthor():
            publications = author.getPublications()
            authorID = author.addAuthorInformations()
            author.addConcepts()
            publicationsAPI = PublicationAPI(publications, self.dataBase, authorID, self.sourceID)
            publicationsAPI.addPublications(5)
        else:
            print("Houlala")
