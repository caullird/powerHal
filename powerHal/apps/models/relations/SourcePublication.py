from apps import db
from sqlalchemy import DateTime

class SourcePublication(db.Model):
    __tablename__ = 'sourcepublication'
    id_sourcepublication = db.Column(db.Integer, primary_key=True)
    id_publication = db.Column(db.Integer)
    id_source = db.Column(db.Integer)
    specificID = db.Column(db.String(500))

