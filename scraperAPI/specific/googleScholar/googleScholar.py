from specific.googleScholar.API.AuthorAPI import AuthorAPI
from specific.googleScholar.API.PublicationAPI import PublicationAPI

from config.ResearchSource import ResearchSource

class googleScholar():

    def __init__(self,dataBase,research):

        self.author_name = research["author_name"]
        self.author_forename = research["author_forename"]
        self.id_connected_user = research["id_connected_user"]
        self.id_author_as_user = research["id_author_as_user"]

        self.dataBase = dataBase
        self.sourceID = ResearchSource("googleScholar", self.dataBase).getMySQLID()
        self.run()

    def run(self):

        author = AuthorAPI(self.author_name, self.author_forename, self.dataBase,self.sourceID)
        if author.findAuthor():
            publications = author.getPublications()
            authorID = author.addAuthorInformations()
            author.addConcepts()
            publicationsAPI = PublicationAPI(publications, self.dataBase, authorID, self.sourceID)
            publicationsAPI.addPublications()
        else:
            print("Houlala")
