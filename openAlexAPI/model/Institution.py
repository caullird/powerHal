from pydoc import classname
from config.DB import DB

class Institution():

    def __init__(self, alexID : str, ror : str, display_name : str, country_code : str, type : str): 
        self.idAlex_institution = alexID
        self.display_name = display_name
        self.country_code = country_code
        self.type_institution = type
        self.idRor_insitution = ror

    def setDataBase(self, database):
        self.database = database

    def checkIfExists(self):
        ## TODO - Automatisation : faire une méthode qui prend en paramètre le nouvel objet et qui test l'ensemble des champs

        if(self.database.checkIfExists("Institution",str("display_name = '" + self.display_name + "' or idAlex_institution = '" + self.idAlex_institution + "'"))): 
            self.insertMySQL()

    def insertMySQL(self):
        ## TODO - Automatisation : faure une méthode qui prend en paramètre l'objet qui l'insert avec le nom des variables de la classe

        sql = "INSERT INTO institution (idAlex_institution, display_name,country_code,type_institution,idRor_insitution) VALUES (%s, %s, %s, %s, %s)"
        val = (self.idAlex_institution, self.display_name, self.country_code, self.type_institution, self.idRor_insitution)
        self.database.makeInsertion(sql, val)

        print("INFO | Une nouvelle institution a été ajouté sur votre base de donnée - " + str(self.display_name))
