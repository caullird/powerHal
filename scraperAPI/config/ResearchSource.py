class ResearchSource():
    def __init__(self, sourceName, DB):
        self.sourceName = sourceName
        self.DB = DB
        self.data = self.getSourceInformations()
        self.MySQLID = self.getMySQLID()
        self.urlAPI = self.getAPIUrl()
    
    def getSourceInformations(self):
        return self.DB.getSourceInformations(self.sourceName)
    
    def getMySQLID(self):
        return self.data[0]

    def getAPIUrl(self):
        return self.data[3]

    
