# -*- encoding: utf-8 -*-

from apps.section.home import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.models.entities.Author import Author
from apps.models.entities.Publication import Publication
from apps.models.relations.AuthorPublication import AuthorPublication
from apps.section.profil.forms import ProfilAuthorForm
from apps import db, login_manager

from flask import Response

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import requests

from flask_login import (
    current_user
)


@blueprint.route('/index')
@login_required
def index():

    if current_user.id_author is None:
        return redirect(url_for('home_blueprint.account'))

    author = Author.query.filter_by(id_author=current_user.id_author,created_by=current_user.id).first()

    countPublication = AuthorPublication.query.filter_by(id_author=current_user.id_author,created_by=current_user.id).count()

    countCitation = 0
    
    for publication in Publication.query.filter_by(created_by=current_user.id).all():
        authorPublications = AuthorPublication.query.filter_by(id_publication=publication.id_publication,created_by=current_user.id,id_author=current_user.id_author).all()
        if authorPublications :
            countCitation += int(publication.citation_count)


    print(current_user.id)
    return render_template('home/dashboard.html', author = author, countPublication = countPublication, countCitation = countCitation, segment='index')


@blueprint.route('/graph.png')
def graph_png():
    img = requests.get("http://localhost:8000/graph/" + str(current_user.id))
    return Response(img, mimetype='image/png')

@blueprint.route('/cloud.png')
def cloud_png():
    img = requests.get("http://localhost:8000/cloud/" + str(current_user.id))
    return Response(img, mimetype='image/png')

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None