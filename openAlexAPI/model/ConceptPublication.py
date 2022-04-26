class ConceptPublication():

    def __init__(self, alexID, wikidata, display_name, level, score):
        self.idAlex_conceptpublication = alexID
        self.wikidata = wikidata
        self.display_name = display_name
        self.level_concept = level
        self.score = score

    # Permet d'ajouter l'objet database à l'objet concept
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        self.database.checkIfExistsOrInsert(self, fieldsComparable = ["idAlex_conceptpublication", "display_name"])



