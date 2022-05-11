# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration

class ExportForm(FlaskForm):

    # Informations relatives à la publication 
    publication_title = StringField('Titre de la publication',
                         id='publication_title',
                         validators=[DataRequired()])

    publication_type = StringField('Type de la publication',
                         id='publication_type',
                         validators=[DataRequired()])

    publication_date = StringField("La date de la publication",
                         id='publication_date',
                         validators=[DataRequired()])
                         
    publication_year = StringField("L'année de la publication",
                         id='publication_year',
                         validators=[DataRequired()])


    # Informations relatives a la bibliographie
    biblio_volume = StringField('Volume bibliographique',
                        id='biblio_volume')

    biblio_first_page = StringField('Première page',
                        id='biblio_first_page')

    biblio_last_page = StringField('Dernière page',
                        id='biblio_last_page')

    biblio_issue = StringField('Biblio issue',
                        id='biblio_issue')


    # Informations relatives à l'auteur
    author_name = StringField('Prénom',
                         id='author_name',
                         validators=[DataRequired()])

    author_forename = StringField('Nom de famille',
                             id='author_forname',
                             validators=[DataRequired()])

    alternative_name = StringField("Alternative d'identification",
                        id='alternatives')
    
    orcid_id = StringField('ORCID ID',
                        id='orcid_id')  

