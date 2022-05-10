# -*- encoding: utf-8 -*-

from flask import render_template, redirect, request, url_for
from apps.section.profil.forms import ProfilAuthorForm
from apps.section.home import blueprint
from flask import render_template
from flask_login import login_required
from apps.models.entities.Author import Author
from apps import db, login_manager

from flask_login import (
    current_user
)


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    
    authorForm = ProfilAuthorForm(request.form)

    author = None
    if(current_user.id_author != None):
        author = Author.query.filter_by(id_author=current_user.id_author).first()

    if 'account' in request.form:
        author_name = request.form['author_name']
        author_forename = request.form['author_forename']
        orcid_id = request.form['orcid_id']
        alternative_name = request.form['alternative_name']

        if author:
            author.author_name = author_name
            author.author_forename = author_forename
            author.display_name = str(sortResearch(author_name+" "+author_forename))
            author.orcid_id = orcid_id
            author.created_by = current_user.id
            author.alternative_name = alternative_name
            current_user.id_author = author.id_author
            db.session.commit()
        else:
            author = Author()
            author.orcid_id = orcid_id
            author.author_forename = author_forename
            author.author_name = author_name
            author.display_name = str(sortResearch(author_name+" "+author_forename))
            author.created_by = current_user.id
            author.alternative_name = alternative_name
            db.session.add(author)
            db.session.commit()

            current_user.id_author = author.id_author
            db.session.commit()


        return render_template('profil/account.html', author = author, form = authorForm, message = "Votre profil est maintenant à jour !", segment='index')

    return render_template('profil/account.html', author = author, form = authorForm, segment='index')

def sortResearch(display_name):
        values = display_name.split()
        values.sort()
        return ' '.join(values)


