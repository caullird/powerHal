from pydoc import classname
from config.DB import DB

class Institution():

    # Permet de créer un objet de type institution
    def __init__(self, display_name : str, country_code : str, type : str): 
        self.display_name = display_name
        self.country_code = country_code
        self.type_institution = type
        #self.idRor_insitution = ror

    # Permet d'ajouter l'objet database à l'objet institution
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet institution existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ["country_code", "display_name"])
