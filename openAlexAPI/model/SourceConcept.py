class SourceConcept():

    def __init__(self,id_concept,id_source,specificId,specificInformation):
        self.id_concept = id_concept
        self.id_source = id_source
        self.specificId = specificId
        # Ranger les informations sous forme d'un mini json
        self.specificInformation = specificInformation

    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['id_concept','id_source'])

