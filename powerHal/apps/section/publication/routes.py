# -*- encoding: utf-8 -*-


from apps.section.home import blueprint
from flask import render_template
from flask_login import login_required
from apps.models.Publication import Publication


@blueprint.route('/publication')
@login_required
def publication():
    return render_template('publications/publications.html', publication = Publication.query.all(), segment='index')


