# -*- encoding: utf-8 -*-

import subprocess
import pathlib
from threading import Thread
from apps.section.home import blueprint
from flask import render_template
from flask_login import login_required
from apps.models.entities.Publication import Publication
from apps.models.entities.Author import Author

from flask_login import (
    current_user
)


@blueprint.route('/scraper')
@login_required
def scraper():
    author = Author.query.filter_by(id_author=current_user.id_author).first()

    return render_template('scraper/scraper.html', author = author , segment='index')


@blueprint.route('/openAlex')
@login_required
def openAlexAPI():
    return render_template('scraper/openAlex.html', segment='index')
