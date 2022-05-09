# -*- encoding: utf-8 -*-

from apps.section.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.models.entities.Author import Author
from apps.section.profil.forms import ProfilAuthorForm
from apps import db, login_manager

from flask import Response

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import random

import requests

from flask_login import (
    current_user
)


@blueprint.route('/index')
@login_required
def index():

    author = Author.query.filter_by(id_author=current_user.id_author).first()


    return render_template('home/dashboard.html', author = author, segment='index')


@blueprint.route('/plot.png')
def plot_png():
    img = requests.get("http://localhost:8000/graph/" + str(current_user.id))
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
