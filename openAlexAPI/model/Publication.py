from pydoc import classname
from config.DB import DB

class Publication():
    # Permet de créer un objet de type publication
    def __init__(self, alexID, doi, title, display_name):
        self.idAlex_publication = alexID
        self.idDoi_publication = doi
        self.title = title
        self.display_name = display_name


    # def __init__(self, alexID, doi, title, display_name, mag, type, publication_year, publication_date, updated_date, created_date):
    #     self.idAlex_publication = alexID
    #     self.idDoi_publication = doi
    #     self.title = title
    #     self.display_name = display_name
    #     self.mag = mag 
    #     self.type_publication = type
    #     self.publication_year = publication_year
    #     self.publication_date = publication_date
    #     self.updated_date = updated_date
    #     self.created_date = created_date



