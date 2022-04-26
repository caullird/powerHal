class AuthorPublicationConcept():

    def __init__(self,idAuthor,idPublication, idConcept):
        self.id_author = idAuthor
        self.id_publication = idPublication
        self.id_concept = idConcept

    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['id_author','id_publication','id_concept'])

