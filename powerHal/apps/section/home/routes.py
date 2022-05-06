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

from flask_login import (
    current_user
)


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

@blueprint.route('/<template>')
@login_required
def route_template(template):

    authorForm = ProfilAuthorForm(request.form)

    author = None
    if(current_user.id_author != None):
        author = Author.query.filter_by(id_author=current_user.id_author).first()

    if 'account' in request.form:
        # read form data
        author_name = request.form['author_name']
        author_forename = request.form['author_forename']

        if author:
            author.author_name = author_name
            author.author_forename = author_forename
            author.display_name = author_name + " " + author_forename
            current_user.id_author = author.id_author
            db.session.commit()
        else:
            author = Author()
            author.author_forename = author_forename
            author.author_name = author_name
            db.session.add(author)
            db.session.commit()

            current_user.id_author = author.id_author
            db.session.commit()

        return render_template('home/dashboard.html', author = author, form = authorForm, message = "Votre profil est maintenant à jour !", segment='index')

    return render_template('home/dashboard.html', author = author, form = authorForm, message = "Votre profil est maintenant à jour !", segment='index')


    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
