class ResearchInitializer():

    def __init__(self,research : str):
        self.initial_research = research

        self.sortResearch = self.sortResearch()
        self.prepareResearch = self.prepareResearch()

    # Permet de généré l'ensemble des possibilités du couple {nom, prénom}
    def sortResearch(self):
        values = self.initial_research.split()
        values.sort()
        return ' '.join(values)

    # Permet de mettre en forme la recherche en paramètre
    def prepareResearch(self):
        specialChars = "!#$%^&*()" 

        result = self.sortResearch

        for specialChar in specialChars:
            result = result.replace(specialChar, '')

        result = result.replace(' ', '-')

        return result.lower()

    
    def getSortResearch(self):
        return self.sortResearch

    def getPrepareResearch(self):
        return self.prepareResearch
