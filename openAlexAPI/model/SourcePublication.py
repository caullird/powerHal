class SourcePublication():

    def __init__(self,id_publication,id_source,specificId):
        self.id_publication = id_publication
        self.id_source = id_source
        self.specificId = specificId

    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['id_publication','id_source','specificId'])

