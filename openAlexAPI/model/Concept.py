class Concept():

    def __init__(self, wikidata, display_name):
        self.wikidata = wikidata
        self.display_name = display_name

    # Permet d'ajouter l'objet database à l'objet concept
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ["display_name"])



