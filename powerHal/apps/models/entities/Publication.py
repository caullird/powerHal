from apps import db

class Publication(db.Model):
    __tablename__ = 'publication'
    id_publication = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    type_publication = db.Column(db.String(500))
    publication_year = db.Column(db.String(500))
    publication_date = db.Column(db.String(500))
    citation_count = db.Column(db.String(500))
    reference_count = db.Column(db.String(500))
    id_source = db.Column(db.Integer)

    biblio_volume = db.Column(db.String(500))
    biblio_first_page = db.Column(db.String(500))
    biblio_last_page = db.Column(db.String(500))
    biblio_issue = db.Column(db.String(500))