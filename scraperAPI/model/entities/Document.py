class Document():

    def __init__(self, id, class_name, document_url, id_source):
        self.id_object = id
        self.class_name = class_name
        self.document_url = document_url 
        self.id_source = id_source

    # Permet d'ajouter l'objet database à l'objet concept
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ["id_object","class_name","document_url"])

