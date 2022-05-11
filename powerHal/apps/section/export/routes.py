# -*- encoding: utf-8 -*-
import json, requests
from apps.section.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.section.export.forms import ExportForm
from apps.models.entities.Publication import Publication
from apps.models.entities.Source import Source
from apps.models.entities.Document import Document
from apps.models.entities.Author import Author
from apps.models.entities.Concept import Concept
from apps.models.relations.AuthorPublication import AuthorPublication
from apps.models.relations.SourcePublication import SourcePublication
from apps.models.relations.AuthorPublicationConcept import AuthorPublicationConcept
from apps import db, login_manager

from flask_login import ( current_user )




@blueprint.route('/export', methods=['GET', 'POST'])
@login_required
def export_loading():

    # Mise en place du formulaire 
    exportForm = ExportForm(request.form)

    # Récupération de l'argument
    page = request.args.get('idPublication', type = int)

    if 'export' in request.form:
        generateFile(page)

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


def generateFile(idPublication):
    pass 
    # TODO : génération du fichier
    # result = json.loads(requests.get("http://127.0.0.1:8000/generateFile/" + str(idPublication) + "/" + str(current_user.id)).json)

    # print(result)