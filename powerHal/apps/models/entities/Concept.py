from apps import db

class Concept(db.Model):
    __tablename__ = 'concept'
    id_concept = db.Column(db.Integer, primary_key=True)
    wikidata = db.Column(db.String(2000))
    display_name = db.Column(db.String(500))
    created_by = db.Column(db.Integer)

