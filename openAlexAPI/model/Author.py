class Author():

    def __init__(self,idsAlexAuthor, orcid_id, display_name, display_name_alternatives, works_count, cited_by_count):
        self.idsAlex_author = idsAlexAuthor
        self.orcid_id = orcid_id
        self.display_name = display_name
        self.display_name_alternatives = display_name_alternatives
        self.works_count = works_count
        self.cited_by_count = cited_by_count

    # Permet d'ajouter l'objet database à l'objet Author
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['display_name'], autoUpdate = False)
