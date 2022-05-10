from apps import db

class Document(db.Model):
    __tablename__ = 'document'
    id_document = db.Column(db.Integer, primary_key=True)
    id_object = db.Column(db.Integer)
    class_name = db.Column(db.String(500))
    document_url = db.Column(db.String(5000))
    id_source = db.Column(db.Integer)
    created_by = db.Column(db.Integer)
    

