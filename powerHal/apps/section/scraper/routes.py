# -*- encoding: utf-8 -*-

import requests
import json
from apps.section.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.models.entities.Publication import Publication
from apps.models.entities.Author import Author

from flask_login import (
    current_user
)

@blueprint.route('/scraper', methods=['GET', 'POST'])
@login_required
def scraper():
    if request.method == 'POST':
        getChoises = request.form.getlist('apiChoise')

        if 'openAlexAPI' in getChoises:
            openAlexAPI() 

        if 'openCitationAPI' in getChoises:
            openCitationAPI()

        if 'googleScholar' in getChoises:
            googleScholar()

    author = Author.query.filter_by(id_author=current_user.id_author).first()
    return render_template('scraper/scraper.html', author = author , segment='index')


def openAlexAPI():
    return json.loads(requests.get("http://127.0.0.1:8000/openAlex/" + str(current_user.id)).text)

def openCitationAPI():
    return json.loads(requests.get("http://127.0.0.1:8000/openCitation/" + str(current_user.id)).text)

def googleScholar():
    return json.loads(requests.get("http://127.0.0.1:8000/googleScholar/" + str(current_user.id)).text)