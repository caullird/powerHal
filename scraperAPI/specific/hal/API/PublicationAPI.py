# Importation des classes pour la configuration globale au projet
import requests
import json
import os

# Importation des modèles pour la création des objets
from model.entities.Institution import Institution
from model.entities.Author import Author
from model.entities.Concept import Concept
from model.entities.Document import Document
from model.relations.AuthorInstitution import AuthorInstitution
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceInstitution import SourceInstitution
from model.relations.SourceConcept import SourceConcept
from model.relations.SourcePublication import SourcePublication

class PublicationAPI():
    
    def __init__(self,dataBase, id_connected_user, id_author_as_user, API, sourceID):
        self.dataBase = dataBase
        self.id_connected_user = id_connected_user
        self.id_author_as_user = id_author_as_user
        self.sourceID = sourceID
        self.API = API
        
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
                        
                        return True
                    
                print("je suis inexistant")
            
            

                headers = {
                    'Packaging': 'http://purl.org/net/sword-types/AOfr',
                    'Content-Type': 'application/zip',
                    'Content-Disposition': 'attachment; filename=meta.xml',
                }

                data = "././scraperAPI/specific/hal/data/depot.zip"
                
                print(os.path.exists(data))

                response = requests.post('https://api-preprod.archives-ouvertes.fr/sword/hal/', headers=headers, data=data, auth=('caullird', 'proj831-hal'))
                
                print(response)
                                    