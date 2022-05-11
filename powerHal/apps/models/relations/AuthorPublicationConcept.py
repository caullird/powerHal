from apps import db
from sqlalchemy import DateTime

class AuthorPublicationConcept(db.Model):
    __tablename__ = 'authorpublicationconcept'
    id_authorpublicationconcept = db.Column(db.Integer, primary_key=True)
    id_author = db.Column(db.Integer)
    id_publication = db.Column(db.Integer)
    id_concept = db.Column(db.Integer)
    level_concept = db.Column(db.String(500))
    score_concept = db.Column(db.String(500))
    created_by = db.Column(db.Integer)

