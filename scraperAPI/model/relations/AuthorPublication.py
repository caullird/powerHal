class AuthorPublication():

    def __init__(self,idAuthor,idPublication,author_position):
        self.id_author = idAuthor
        self.id_publication = idPublication
        self.author_position = author_position

    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['id_author','id_publication'])

