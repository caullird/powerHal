from pydoc import classname
from config.DB import DB

class Publication():

    # Permet de créer un objet de type publication
    def __init__(self, doi, title, display_name, type, publication_year, publication_date, updated_date, created_date):
        self.id_doi = doi
        self.title = title
        self.display_name = display_name
        self.type_publication = type
        self.publication_year = publication_year
        self.publication_date = publication_date
        self.updated_date = updated_date
        self.created_date = created_date

    # Permet d'ajouter l'objet database à l'objet publication
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet publication existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ["publication_year", "display_name"])

