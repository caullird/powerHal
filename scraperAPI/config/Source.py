class Source():
    def __init__(self, sourceName, DB):
        self.sourceName = sourceName
        self.DB = DB
        self.MySQLID = self.researchMySQLID()
    
    def researchMySQLID(self):
        return self.DB.getSourceID(self.sourceName)
    
    def getMySQLID(self):
        return self.MySQLID
    

    
