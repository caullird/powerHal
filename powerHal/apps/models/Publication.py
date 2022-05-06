from apps import db

class Publication(db.Model):
    __tablename__ = 'publication'
    id_publication = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    type_publication = db.Column(db.String(500))
    publication_year = db.Column(db.String(500))
    citation_count = db.Column(db.String(500))
    reference_count = db.Column(db.String(500))