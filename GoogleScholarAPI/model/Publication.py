class Publication():

    def __init__(self,titre, pub_date, description,autheur,affiliation, pdf_lien):
        self.titre = titre
        self.pub_date = pub_date
        self.description = description
        self.autheur = autheur
        self.affiliation = affiliation
        self.pdf_lien = pdf_lien

    def get_info(self):
        return self.titre, self.pub_date, self.description, self.autheur, self.affiliation, self.pdf_lien
