from specific.googleScholar.API.AuthorAPI import AuthorAPI
from specific.googleScholar.API.PublicationAPI import PublicationAPI

from config.ResearchSource import ResearchSource
from config.DB import DB

class googleScholar():

    def __init__(self,research):
        self.research = research
        self.dataBase = DB()
        self.dataBase.setConnectedUserId(research['id_connected_user'])
        self.run()

    def run(self):
        source = ResearchSource("googleScholar", self.dataBase)
        sourceID = source.getMySQLID()
        sourceAPIURL = source.getAPIUrl()

        author = AuthorAPI(self.research, self.dataBase,sourceID)
        if author.findAuthor():
            publications = author.getPublications()
            authorID = author.addAuthorInformations()
            author.addConcepts()
            publicationsAPI = PublicationAPI(publications, self.dataBase, authorID, sourceID)
            publicationsAPI.addPublications()
