from apps import db
from sqlalchemy import DateTime

class AuthorPublication(db.Model):
    __tablename__ = 'authorpublication'
    id_authorPublication = db.Column(db.Integer, primary_key=True)
    id_author = db.Column(db.Integer)
    id_publication = db.Column(db.Integer)
    author_position = db.Column(db.String(500))
    created_by = db.Column(db.Integer)

