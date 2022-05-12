# -*- coding: utf-8 -*-
import json, requests, os, shutil, subprocess
from numpy import source
from apps import db, login_manager

from apps.section.home import blueprint
from flask import render_template, request
from flask_login import login_required
from apps.section.export.forms import ExportForm

# Importation des models pour les entities
from apps.models.entities.Publication import Publication
from apps.models.entities.Source import Source
from apps.models.entities.Document import Document
from apps.models.entities.Author import Author
from apps.models.entities.Concept import Concept

# Importation des models pour les relations
from apps.models.relations.AuthorPublication import AuthorPublication
from apps.models.relations.SourcePublication import SourcePublication
from apps.models.relations.AuthorPublicationConcept import AuthorPublicationConcept

from flask_login import ( current_user )


# Affichage de la vue pour centraliser les informations et les modifier (in progress)
@blueprint.route('/export', methods=['GET', 'POST'])
@login_required
def export_loading():

    # Mise en place du formulaire 
    exportForm = ExportForm(request.form)

    # Récupération de l'argument
    page = request.args.get('idPublication', type = int)

    if 'export' in request.form:
        return generateFile(page)

    # Récupération des publications
    publication = Publication.query.filter_by(id_publication=page).first()

    # Récupération des documents
    documents = Document.query.filter_by(id_object=page, class_name = "Publication").all()

    # Récupération des auteurs
    author = Author.query.filter_by(id_author=current_user.id_author).first()

    # Récupération des sources
    sources = []
    for source in Source.query.all():
        sources.append(source.display_name)

    # Verification si la publication existe sur HAL
    existHal = False
    for sourcePublication in SourcePublication.query.filter_by(id_publication=page).all():
        if sourcePublication.id_source == 4:
            existHal = True

    # Récupération des co-auteurs
    co_authors = []
    authorPublication = AuthorPublication.query.filter_by(id_publication=page).all()
    for author in authorPublication:
        co_authors.append([Author.query.filter_by(id_author=author.id_author).first(),author.author_position])

    # Récupération des concepts 
    concepts = []
    publicationConcept = AuthorPublicationConcept.query.filter_by(id_publication=page).all()
    for concept in publicationConcept:
        concepts.append(Concept.query.filter_by(id_concept=concept.id_concept).first())


    return render_template('export/prepareExport.html', form = exportForm, author = author, concepts = concepts, publication = publication, documents = documents, co_authors = co_authors, sources = sources, existHal = existHal, segment='index')

# Permet de générer le fichier XML
def generateFile(idPublication):
    publication = Publication.query.filter_by(id_publication=idPublication).first()

    authorsPublication = AuthorPublication.query.filter_by(id_publication=idPublication).all()

    conceptPublications = AuthorPublicationConcept.query.filter_by(id_publication=idPublication).all()

    file = f'''
            <text>
                <body>
                    <listBibl>
                        <biblFull>
                            <titleStmt>'''

    file += '<title xml:lang="en">' + publication.title + '</title>'

    for authorPublication in authorsPublication:
        author = Author.query.filter_by(id_author=authorPublication.id_author).first()

        role = authorPublication.author_position
        if authorPublication.author_position not in ['first','middle']:
            role = 'middle'

        file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(author.author_forename)}</forename>
                    <surname>{str(author.author_name)}</surname>
                </persName>
                <email>mail@gmail.com</email>
                <ptr type="url" target="https://www.univ-smb.fr/listic/"/>
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

    file += '<title xml:lang="en">' + publication.title + '</title>'

    for authorPublication in authorsPublication:
        author = Author.query.filter_by(id_author=authorPublication.id_author).first()

        role = authorPublication.author_position
        if authorPublication.author_position not in ['first','middle']:
            role = 'middle'

        file += f'''             
            <author role="{ role }">
                <persName>
                    <forename type="first">{str(author.author_forename)}</forename>
                    <surname>{str(author.author_name)}</surname>
                </persName>
                <email>mail@gmail.com</email>
                <ptr type="url" target="https://www.univ-smb.fr/listic/"/>
                <affiliation ref="#struct-1"/>
            </author>'''
    file += "</analytic>"

    # Ecriture des informations relative a la bibliographie
    file += f'''
        <monogr>
            <idno type="localRef"></idno>
            <idno type="halJournalId">2872</idno>
            <imprint>
                <biblScope unit="volume">{publication.biblio_volume}</biblScope>
                <biblScope unit="pp">{publication.biblio_first_page} - {publication.biblio_last_page}</biblScope>
                <date type="datePub">{publication.publication_year}</date>
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

    for conceptPublication in conceptPublications:
        concept = Concept.query.filter_by(id_concept=conceptPublication.id_concept).first()
        file += f'''
            <term xml:lang="en">{ concept.display_name }</term>'''

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
    </text>'''

    path = "apps/data/publications/" + str(idPublication) + "/" + "result.xml"
    if not os.path.exists("apps/data/publications/" + str(idPublication)):
        os.makedirs("apps/data/publications/" + str(idPublication))


    saveFile = open(path,"w") 
    saveFile.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
    saveFile.write('<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:hal="http://hal.archives-ouvertes.fr/">')
    saveFile.write(file)
    saveFile.write('</TEI>')
    saveFile.close()

    document = Document.query.filter_by(id_object=idPublication, class_name = "Publication").first()

    download_file(document.document_url, "DOC.pdf", idPublication)

    pathZip = str("apps/data/publications/" + str(idPublication))

    # zipFile = shutil.make_archive(pathZip + "/" + str(idPublication), 'zip', pathZip)

    zipFile = shutil.make_archive("depot", 'zip', pathZip)

    insertHAL(idPublication)

    insertRelationSourcePublication(idPublication)

    return render_template('export/resultExport.html')

# Permet de récupérer le fichier pdf depuis le site source de l'article
def download_file(download_url, filename, idPublication):
    r = requests.get(download_url, stream=True)
    with open('apps/data/publications/' + str(idPublication) + '/DOC.pdf', 'wb') as f:
        f.write(r.content)
        f.close()

# Permet d'ajouter les informations dans HAL
def insertHAL(idPublication):
    zip = "apps/data/publications/" + str(idPublication) + "/" + str(idPublication) + ".zip"
    CurlUrl = 'curl -v -u caullird:proj831-hal https://api.archives-ouvertes.fr/sword/hal/ -H "Packaging:http://purl.org/net/sword-types/AOfr" -X POST -H "Content-Type:application/zip" -H "Content-Disposition: attachment; filename=result.xml" --data-binary @depot.zip'
    status, output = subprocess.getstatusoutput(CurlUrl)

# Permet de faire la relation entre HAL et la publication
def insertRelationSourcePublication(idPublication):
    sourcePublication = SourcePublication()
    sourcePublication.id_publication = idPublication
    sourcePublication.id_source = 4
    db.session.commit()