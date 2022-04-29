class Source():

    def __init__(self,display_name,website_url, api_url):
        self.display_name = display_name
        self.website_url = website_url
        self.api_url = api_url

    def setDataBase(self, database):
        self.database = database

    # Permet de vérifier si l'objet concept existe dans la base de données et l'ajouter dans le cas échéant
    def checkIfExistsOrInsert(self):
        return self.database.checkIfExistsOrInsert(self, fieldsComparable = ['display_name'])

