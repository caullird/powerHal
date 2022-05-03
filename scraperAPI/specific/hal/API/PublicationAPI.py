# Importation des classes pour la configuration globale au projet
import requests
import json
import subprocess

# Importation des modèles pour la création des objets
from model.entities.Document import Document
from model.relations.SourcePublication import SourcePublication

class PublicationAPI():
    
    def __init__(self,dataBase, id_connected_user, id_author_as_user, API, sourceID):
        self.dataBase = dataBase
        self.id_connected_user = id_connected_user
        self.id_author_as_user = id_author_as_user
        self.sourceID = sourceID
        self.API = API
        
        # self.checkIfInsert()
        self.tryToInsert()
        
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
                
                #unSourcePublication = SourcePublication(getPublication[0],self.sourceID)
                result = json.loads(requests.get(self.API.getUrlAPI() + "?q=" + str(getPublication[1])).text)
                
                # Si il existe un resultat sur Hal
                if result['response']['numFound'] != 0:
                    for element in result['response']['docs']:
                        
                        # Ajoute un lien entre une source et une publication
                        unSourcePublication = SourcePublication(getPublication[0],self.sourceID,element['docid'], "{}")
                        unSourcePublication.setDataBase(self.dataBase)
                        unSourcePublication.checkIfExistsOrInsert()

                        # Ajoute un document
                        unDocument = Document(getPublication[0],"Publication",element['uri_s'], self.sourceID)
                        unDocument.setDataBase(self.dataBase)
                        unDocument.checkIfExistsOrInsert()
            else : 
                print("je suis inexistant")

                # Génération du fichier XML
                self.generateXML()

                # Verfication si présence de PDF
                self.getPublicationPDF()
                 
                # Génération de l'archive zip
                self.generateZIP()

                # Importation du document dans hal
                self.importDocument()
                

    # Fonction qui permet de générer un fichier XML     
    def generateXML(self):
        pass

    # Fonction qui permet de récupérer un fichier PDF d'une publication 
    def getPublicationPDF(self):    
        pass

    # Fonction qui permet de générer un ZIP
    def generateZIP(self):
        pass

    # Fonction qui permet d'importer un document dans HAL
    def importDocument(self):
        pass


    def tryToInsert(self):

        # TODO : changer la requête curl en une request()

        CurlUrl = 'curl -v -u caullird:proj831-hal https://api.archives-ouvertes.fr/sword/hal/ -H "Packaging:http://purl.org/net/sword-types/AOfr" -X POST -H "Content-Type:application/zip" -H "Content-Disposition: attachment; filename=meta.xml" --data-binary @depot.zip'

        status, output = subprocess.getstatusoutput(CurlUrl)

        
