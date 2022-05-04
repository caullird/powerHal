class Publication():

    # Permet de créer un objet de type publication
    def __init__(self, doi, title, display_name, type, publication_year, publication_date, biblio_volume, biblio_first_page, biblio_last_page, biblio_issue, updated_date, created_date, id_source, citation_count):
        self.id_doi = doi
        self.title = title
        self.display_name = display_name
        self.type_publication = type
        self.publication_year = publication_year
        self.publication_date = publication_date
        self.biblio_volume = biblio_volume 
        self.biblio_first_page = biblio_first_page
        self.biblio_last_page = biblio_last_page
        self.biblio_issue = biblio_issue
        self.updated_date = updated_date
        self.created_date = created_date
        self.id_source = id_source
        self.citation_count = citation_count
        self.reference_count = 0

    # Permet d'ajouter l'objet database à l'objet publication
    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet publication existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ["publication_year", "display_name","id_source"])

    def show(self):
        print("id_doi: " + str(self.id_doi))
        print("title: " + str(self.title))
        print("display_name: " + str(self.display_name))
        print("type_publication: " + str(self.type_publication))
        print("publication_year: " + str(self.publication_year))
        print("publication_date: " + str(self.publication_date))
        print("biblio_volume: " + str(self.biblio_volume))
        print("biblio_first_page: " + str(self.biblio_first_page))
        print("biblio_last_page: " + str(self.biblio_last_page))
        print("biblio_issue: " + str(self.biblio_issue))
        print("updated_date: " + str(self.updated_date))
        print("created_date: " + str(self.created_date))
        print("id_source: " + str(self.id_source))
        print("citation_count: " + str(self.citation_count))
        print("reference_count: " + str(self.reference_count))