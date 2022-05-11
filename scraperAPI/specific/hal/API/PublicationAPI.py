# Importation des classes pour la configuration globale au projet
import requests
import json
import subprocess
import os
import xml.etree.ElementTree as ET 

# Importation des modèles pour la création des objets
from model.entities.Document import Document
from model.relations.SourcePublication import SourcePublication

class PublicationAPI():
    
    def __init__(self,dataBase, research, urlAPI, sourceID):
        self.dataBase = dataBase
        self.id_connected_user = research['id_connected_user']
        self.id_author_as_user = research['id_author_as_user']
        self.sourceID = sourceID
        self.urlAPI = urlAPI
        
        self.checkIfInsert()
        
    def checkIfInsert(self):
        # Récupération de l'ensemble des publications de l'auteur
        getAuthorPublications = self.dataBase.getFieldsWithId(self.id_author_as_user, "AuthorPublication","id_author","id_publication","many")
        
        for publication in getAuthorPublications:
            # Verification si il y a déjà un lien avec la source et la publication
            
            # TODO : permet d'éviter de passer du temps pour pas grand chose
            
            # Récupération des informations de la publication
            getPublication = self.dataBase.getFieldsWithId(publication, "Publication","id_publication","*","one")
            
            # Verification si présence d'un doi
            if getPublication[1] not in ["","[]","{}","()","NULL","None"]:
                request = self.urlAPI + "?q=" + str(getPublication[1])
                result = json.loads(requests.get(request).text)
                isInsert = self.addInDataBase(result, getPublication)

            
            request = self.urlAPI + '?q=title_t:"' + str(getPublication[3]) + '"'
            result = json.loads(requests.get(request).text)
            self.addInDataBase(result, getPublication)
         
    def addInDataBase(self, result, getPublication):   
        # Si il existe un resultat sur Hal
        if result['response']['numFound'] != 0:
            for element in result['response']['docs']:
                
                # Ajoute un lien entre une source et une publication
                unSourcePublication = SourcePublication(getPublication[0],self.sourceID,element['docid'], "{}")
                unSourcePublication.setDataBase(self.dataBase)
                idSourcePublication = unSourcePublication.checkIfExistsOrInsert()

                # Ajoute un document
                unDocument = Document(getPublication[0],"Publication",element['uri_s'], self.sourceID)
                unDocument.setDataBase(self.dataBase)
                unDocument.checkIfExistsOrInsert()

                #  id, table, field, value
                self.dataBase.updateOneField(getPublication[0],"Publication","id_doi",element['docid'])

                return

    def tryToInsert(self):

        # TODO : changer la requête curl en une request()

        CurlUrl = 'curl -v -u caullird:proj831-hal https://api.archives-ouvertes.fr/sword/hal/ -H "Packaging:http://purl.org/net/sword-types/AOfr" -X POST -H "Content-Type:application/zip" -H "Content-Disposition: attachment; filename=meta.xml" --data-binary @depot.zip'

        status, output = subprocess.getstatusoutput(CurlUrl)

        
