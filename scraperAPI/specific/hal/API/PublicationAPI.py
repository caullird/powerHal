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
        # self.path = "././scraperAPI/specific/hal/data/"
        
        self.checkIfInsert()
        # self.tryToInsert()
        
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
                result = json.loads(requests.get(self.urlAPI + "?q=" + str(getPublication[1])).text)
                
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
                # Generate dataFile 
                # self.generateDataFile(getPublication[0])

                # Génération du fichier XML
                # self.generateXML(getPublication)

                return

                # Verfication si présence de PDF
                self.getPublicationPDF()
                 
                # Génération de l'archive zip
                self.generateZIP()

                # Importation du document dans hal
                self.importDocument()

    # Fonction qui permet de générer les fichiers de données
    def generateDataFile(self, id_publication):
        path = self.path + str(id_publication)
        if not os.path.exists(path): os.makedirs(path)     

    # Fonction qui permet de générer un fichier XML     
    def generateXML(self, publication):
        print(publication)
        # Récupération des données de l'auteur
        authors = self.dataBase.autoJoinner(relativeID = publication[0], researchFieldRelativeID = "Publication.id_publication", pathEntitiesRelations = ['Publication','AuthorPublication','Author'], fields = "Author.*, AuthorPublication.author_position")


        file = f'''
        <text>
            <body>
                <listBibl>
                    <biblFull>
                        <titleStmt>'''

        file += '<title xml:lang="en">' + publication[3] + '</title>'

        # Ecriture des informations de chaque auteur (titleStmt)
        for author in authors:

            # TODO : changer le split, en fonction des données rentrée par l'utilisateur
            
            split = author[2].split(" ")

            role = str(author[10])
            if role not in ['first','middle']:
                role = 'middle'


            # <idno type="ORCID">{ str(author[1]) }</idno>
            
            file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(split[0])}</forename>
                    <surname>{str(split[1])}</surname>
                </persName>
                <email>mail@gmail.com</email>
                <ptr type="url" target="http://lkb.cnrs.fr"/>
                <affiliation ref="#struct-1"/>
            </author>'''

        file += "</titleStmt>"

        # Ecriture des informations relative à l'édition
        file += f'''
        <editionStmt>
            <edition>
                <ref type="src" target="paper.zip" subtype="author" n="1"/>
            </edition>
        </editionStmt>'''

        # Ecriture des informations relative a la série
        file += f'''
        <seriesStmt>
            <idno type="stamp" n="LKB"/>
        </seriesStmt>'''


        # Ecriture des informations relative à la source 
        file += f'''
        <sourceDesc>         
            <biblStruct>
                <analytic>
        '''

        file += '<title xml:lang="en">' + publication[3] + '</title>'

        # Ecriture des informations de chaque auteur pour la bibliographie
        for author in authors:

            # TODO : changer le split, en fonction des données rentrée par l'utilisateur
            
            role = str(author[10])
            if role not in ['first','middle']:
                role = 'middle'

            split = author[2].split(" ")
            file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(split[0])}</forename>
                    <surname>{str(split[1])}</surname>
                </persName>
                <email>mail@gmail.com</email>
                <ptr type="url" target="http://lkb.cnrs.fr"/>
                <affiliation ref="#struct-1"/>
            </author>'''
        file += "</analytic>"

        # Ecriture des informations relative a la bibliographie

        file += f'''
        <monogr>
            <idno type="localRef"></idno>
            <idno type="halJournalId">2872</idno>
            <imprint>
                <biblScope unit="volume">{publication[7]}</biblScope>
                <biblScope unit="pp">{publication[8]} - {publication[9]}</biblScope>
                <date type="datePub">{publication[5]}</date>
            </imprint>
        </monogr>
        '''

        file += f'''
            </biblStruct>
        </sourceDesc>
        '''

        # Ecriture des informations relative au profil
        file += f'''
        <profileDesc>
            <langUsage>
                <language ident="en"/>
            </langUsage>
            <textClass>
                <keywords scheme="author">
        '''


        concepts = self.dataBase.autoJoinner(relativeID = publication[0], researchFieldRelativeID = "Publication.id_publication", pathEntitiesRelations = ['Publication','AuthorPublicationConcept','Concept'], fields = "Concept.*")

        for concept in concepts:
            file += f'''
            <term xml:lang="en">{ concept[2] }</term>'''
        
        file += '''
                </keywords>
                <classCode scheme="classification">03.65.Ta, 03.65.ud, 03.67.a</classCode>
                <classCode scheme="halDomain" n="phys.qphy"/>
                <classCode scheme="halDomain" n="shs.hisphilso"/>
                <classCode scheme="halTypology" n="ART"/>
            </textClass>
            <abstract xml:lang="en">No abstract for this document</abstract>
        </profileDesc>'''


        # End of file
        file += '''
                    </biblFull>
                </listBibl>
            </body>
            <back>
                <listOrg type="structures">
                    <org type="laboratory" xml:id="struct-1"/>
                </listOrg>
            </back>
        </text>
        '''


        self.xmlToTEI(file)
        # Partie de titleStmt 
        # tree_model_xml.find("./body/listBibl/biblFull/titleStmt/title").text = publication[3]

        # Partie de l'editionStml 

        # Partie de l'editionStml

        # Partie de notesStml

        # Partie de sourceDesc

        # Partie de profileDesc
    
        #tree_model_xml.write(self.path + "models/test.xml")



        
    def xmlToTEI(self, txt):
        path_result = self.path + "publication/result.xml"
        file = open(path_result,"w") 
        file.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
        file.write('<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">')
        file.write(txt)
        file.write('</TEI>')
        file.close()


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

        
