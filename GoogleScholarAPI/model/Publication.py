class Publication():

    def __init__(self,titre, pub_date, description,author,affiliation, pdf_lien):
        self.titre = titre
        self.pub_date = pub_date
        self.description = description
        self.author = author
        self.affiliation = affiliation
        self.pdf_lien = pdf_lien

    def get_infos(self):
        return self.titre, self.pub_date, self.description, self.author, self.affiliation, self.pdf_lien
