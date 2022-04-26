from config.DB import DB

class Institution():

    def __init__(self, alexID : str, ror : str, display_name : str, country_code : str, type : str): 
        self.alexID = alexID
        self.ror = ror
        self.display_name = display_name
        self.country_code = country_code
        self.type = type

    def setDataBase(self, database):
        self.database = database

    def checkIfExists(self):
        ## TODO : verifier si existe pour ensuite faire update ou insert 

        

        self.insertMySQL()

    def insertMySQL(self):
        sql = "INSERT INTO institution (idAlex_institution, display_name,country_code,type_institution,idRor_insitution) VALUES (%s, %s, %s, %s, %s)"
        val = (self.alexID, self.display_name, self.country_code, self.type, self.ror)

        self.database.makeInsertion(sql, val)

    def updateMySQL(): 
        return "TODO"
