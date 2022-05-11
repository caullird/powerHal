# -*- encoding: utf-8 -*-

import requests, json
from apps.section.home import blueprint
from flask import render_template, request
from flask_login import login_required
from apps.models.entities.Publication import Publication
from apps.models.entities.Source import Source
from apps.models.entities.Document import Document
from apps.models.entities.Author import Author
from apps.models.relations.AuthorPublication import AuthorPublication
from apps.models.relations.SourcePublication import SourcePublication


from flask_login import (
    current_user
)



@blueprint.route('/publication')
@login_required
def publication():

    publications = []
    for publicationID in AuthorPublication.query.filter_by(id_author=current_user.id_author).all():
        publications.append(Publication.query.filter_by(id_publication=publicationID.id_publication).first())

    sources = []
    for source in Source.query.all():
        sources.append(source.display_name)

    sourcePublications = SourcePublication.query.filter_by(id_source=4,created_by=current_user.id).all()
    documents =  Document.query.filter_by(id_source=4,created_by=current_user.id, class_name = "Publication").all()

    return render_template('publications/publications.html', sourcePublications = sourcePublications, publication = publications, documents = documents, sources = sources, segment='index')


@blueprint.route('/viewPublication')
@login_required
def viewPublication():
    page = request.args.get('idPublication', type = int)

    publication = Publication.query.filter_by(id_publication=page).first()

    documents = Document.query.filter_by(id_object=page, class_name = "Publication").all()

    sources = []
    for source in Source.query.all():
        sources.append(source.display_name)

    existHal = False
    for sourcePublication in SourcePublication.query.filter_by(id_publication=page).all():
        if sourcePublication.id_source == 4:
            existHal = True

    co_authors = []
    authorPublication = AuthorPublication.query.filter_by(id_publication=page).all()
    for author in authorPublication:
        co_authors.append(Author.query.filter_by(id_author=author.id_author).first())


    return render_template('publications/viewPublication.html', publication = publication, documents = documents, co_authors = co_authors, sources = sources, existHal = existHal, segment='index')

@blueprint.route('/halCompare')
@login_required
def hal():
    json.loads(requests.get("http://127.0.0.1:8000/halCompare/" + str(current_user.id)).text)
    return publication()
