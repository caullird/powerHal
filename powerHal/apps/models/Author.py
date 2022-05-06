from apps import db
from sqlalchemy import DateTime

class Author(db.Model):
    __tablename__ = 'author'
    id_author = db.Column(db.Integer, primary_key=True)
    orcid_id = db.Column(db.String(2000))
    author_name = db.Column(db.String(500))
    author_forname = db.Column(db.String(500))
    display_name = db.Column(db.String(2000))
