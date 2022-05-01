from apps import db

class Publication(db.Model):
    __tablename__ = 'publication'
    id_publication = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), unique=True)
    type_publication = db.Column(db.String(500), unique=True)
    publication_year = db.Column(db.String(500), unique=True)
    citation_count = db.Column(db.String(500), unique=True)
    reference_count = db.Column(db.String(500), unique=True)