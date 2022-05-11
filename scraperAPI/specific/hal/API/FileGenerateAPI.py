# Importation des classes pour la configuration globale au projet
from config.DB import DB
from config.ResearchSource import ResearchSource
import xml.etree.ElementTree as ET

import os

class FileGenerateAPI():
    
    def __init__(self, research):
        self.dataBase = DB()
        self.dataBase.setConnectedUserId(research['id_connected_user']) 
        self.publicationID = research['id_publication']
        self.generateXML()
    
    # Fonction qui permet de générer un fichier XML     
    def generateXML(self):
        
        publication = self.dataBase.getFieldsWithId(self.publicationID, "Publication","id_publication","*","one")

        authors = self.dataBase.autoJoinner(relativeID = publication[0], researchFieldRelativeID = "Publication.id_publication", pathEntitiesRelations = ['Publication','AuthorPublication','Author'], fields = "Author.*, AuthorPublication.author_position")

        concepts = self.dataBase.autoJoinner(relativeID = publication[0], researchFieldRelativeID = "Publication.id_publication", pathEntitiesRelations = ['Publication','AuthorPublicationConcept','Concept'], fields = "Concept.*")


        return publication, authors, concepts
        file = f'''
        <TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">
        <?xml version="1.0" encoding="UTF-8"?>
            <text>
                <body>
                    <listBibl>
                        <biblFull>
                            <titleStmt>'''

        file += '<title xml:lang="en">' + publication[3] + '</title>'

        # Ecriture des informations de chaque auteur (titleStmt)
        for author in authors:
            role = str(author[10])
            if role not in ['first','middle']:
                role = 'middle'


            # <idno type="ORCID">{ str(author[1]) }</idno>
            
            file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(author[3])}</forename>
                    <surname>{str(author[2])}</surname>
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
            
            role = str(author[10])
            if role not in ['first','middle']:
                role = 'middle'

            file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(author[3])}</forename>
                    <surname>{str(author[2])}</surname>
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

        file += "</TEI>"
        return file 
        

    