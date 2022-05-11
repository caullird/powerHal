# Importation de librairies pour la gestion des PowerCloud
from sqlalchemy import null
from wordcloud import WordCloud
from PIL import Image

# Importation de librairies utiles au bon fonctionnement de la classe
import inspect
import os
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


class PowerCloud():

    def __init__(self, DB):
        self.DB = DB
        self.mask = null


    # Permet de générer le nuage de mots pour les concept des publications d'un auteur en général
    def generatePublicationConcept(self, authorID):
        concepts =  []

        getPublications = self.DB.getFieldsWithId(authorID, table = "AuthorPublication",searchField = "id_author", getField = "id_publication", quantity = "many")
        for publication in getPublications:
            getPublicationConcept = self.DB.getFieldsWithId(publication, table = "AuthorPublicationConcept",searchField = "id_publication", getField = "id_concept", quantity = "many")
            for publicationConcept in getPublicationConcept:
                getConcept = self.DB.getFieldsWithId(publicationConcept, table = "Concept",searchField = "id_concept", getField = "display_name", quantity = "one")
                concepts.append(str(getConcept))

        return self.savePowerCloud(concepts)

    # Permet de générer le nuage de mot pour le lien entre les auteur et les co-auteurs
    def generatePublicationCoAuthors(self, authorID):
        authors = []

        getPublications = self.DB.getFieldsWithId(authorID, table = "AuthorPublication",searchField = "id_author", getField = "id_publication", quantity = "many")
        for publication in getPublications:
            getPublicationAuthors = self.DB.getFieldsWithId(publication, table = "AuthorPublication",searchField = "id_publication", getField = "id_author", quantity = "many")
            for publicationAuthor in getPublicationAuthors:
                getAuthor = self.DB.getFieldsWithId(publicationAuthor, table = "Author",searchField = "id_author", getField = "display_name", quantity = "one")
                authors.append(str(getAuthor))

        
        path = "author" + str(authorID) + "/" + str(inspect.currentframe().f_code.co_name)
        
        return self.savePowerCloud(authors, path)

    # Permet d'enregistrer les nuages de mots dans l'arborescence
    def savePowerCloud(self, concepts):
        #maskArray = np.array(Image.open(self.mask))
        word_could_dict = Counter(concepts)
        #wordcloud = WordCloud(background_color = "white",max_words = len(word_could_dict), mask = maskArray).generate_from_frequencies(word_could_dict)
        wordcloud = WordCloud(background_color = "white",max_words = len(word_could_dict), width=1920, height=1080).generate_from_frequencies(word_could_dict)

        img = wordcloud.to_image()

        return img


