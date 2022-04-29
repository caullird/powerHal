# -*- encoding: utf-8 -*-


from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.publication.models import Publications


@blueprint.route('/publication')
@login_required
def publication():
    return render_template('publications/publications.html', publication = Publications.query.all(), segment='index')


