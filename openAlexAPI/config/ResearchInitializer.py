
class ResearchInitializer():

    def __init__(self,research : str):
        self.initial_research = research
        self.intializedResearch = self.initializeResearch()
    
    # Permet de récupérer le résultat de l'Initializer
    def getInitializeResearch(self):
        return self.intializedResearch

    # Permet de mettre en forme la recherche en paramètre
    def initializeResearch(self):
        specialChars = "!#$%^&*()" 

        result = self.initial_research

        for specialChar in specialChars:
            result = result.replace(specialChar, '')

        result = result.replace(' ', '-')

        return result.lower()