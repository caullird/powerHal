# -*- encoding: utf-8 -*-


from apps.section.home import blueprint
from flask import render_template
from flask_login import login_required
from apps.models.Publication import Publication

from flask_login import (
    current_user,
    login_user,
    logout_user
)


@blueprint.route('/account')
@login_required
def account():
    print(current_user.id_author)
    return render_template('profil/account.html', segment='index')


