# -*- encoding: utf-8 -*-

from flask import render_template, redirect, request, url_for
from apps.section.profil.forms import ProfilAuthorForm
from apps.section.home import blueprint
from flask import render_template
from flask_login import login_required
from apps.models.Author import Author
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
        # read form data
        author_name = request.form['author_name']
        author_forname = request.form['author_forname']
        orcid_id = request.form['orcid_id']

        if author:
            author.author_name = author_name
            author.author_forname = author_forname
            author.display_name = author_name + " " + author_forname
            author.orcid_id = orcid_id
            current_user.id_author = author.id_author
            db.session.commit()
        else:
            author = Author()
            author.orcid_id = orcid_id
            author.author_forname = author_forname
            author.author_name = author_name
            db.session.add(author)
            db.session.commit()

            current_user.id_author = author.id_author
            db.session.commit()


        return render_template('profil/account.html', author = author, form = authorForm, message = "Votre profil est maintenant à jour !", segment='index')

    return render_template('profil/account.html', author = author, form = authorForm, segment='index')


