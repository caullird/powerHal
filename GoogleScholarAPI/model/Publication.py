class Publication():

    def __init__(self,database, id_scholar):
        self.database = database
        self.id_scholar = id_scholar

    def set_infos(self, titre, pub_date, description,author,affiliation, pdf_lien):
        self.titre = titre
        self.pub_date = pub_date
        self.description = description
        self.author = author
        self.affiliation = affiliation
        self.pdf_lien = pdf_lien

    def get_infos(self):
        return self.titre, self.pub_date, self.description, self.author, self.affiliation, self.pdf_lien

    # Permet d'ajouter l'objet database à l'objet Publication
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['id_scholar'])


