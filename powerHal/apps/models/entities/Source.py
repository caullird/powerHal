from apps import db

class Source(db.Model):
    __tablename__ = 'source'
    id_source = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    api_url = db.Column(db.String(500))