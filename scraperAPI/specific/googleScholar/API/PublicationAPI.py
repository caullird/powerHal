from scholarly import scholarly
import requests

# Importation des modèles pour la création des objets
from model.entities.Concept import Concept
from model.entities.Author import Author
from model.entities.Publication import Publication
from model.entities.Document import Document
from model.relations.AuthorPublication import AuthorPublication
from model.relations.AuthorPublicationConcept import AuthorPublicationConcept
from model.relations.SourcePublication import SourcePublication
from model.relations.SourceAuthor import SourceAuthor
from model.relations.SourceConcept import SourceConcept


class PublicationAPI:

    def __init__(self, publications, database, authorID, sourceID):
        self.publications = publications
        self.dataBase = database
        self.authorID = authorID
        self.sourceID = sourceID

    def addPublications(self, max):
        for publication in self.publications[:max]:
            self.checkIfExistOrAdd(publication)

    def checkIfExistOrAdd(self, publication):
        tempPublication = Publication("NULL",publication["bib"]["title"],"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL")
        if self.dataBase.checkIfExists(tempPublication, fieldsComparable = ["title"]):
            return True
        else:
            filledPublication = scholarly.fill(publication)
            url = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=" + filledPublication["author_pub_id"].split(":")[0] + "&citation_for_view=" + filledPublication["author_pub_id"]
            html_page = requests.get(url).text

            try:
                date = html_page.split('<div class="gsc_oci_value">')[2].split("</div>")[0]
            except:
                date = "NULL"

            try:
                volume = filledPublication["bib"]["volume"]
                pages = filledPublication["bib"]["pages"].split("-")
            except:
                volume = "NULL"
                pages = ["NULL","NULL"]

            unePublication = Publication("NULL", filledPublication["bib"]["title"],filledPublication["bib"]["title"],"NULL", filledPublication["bib"]["pub_year"],date,volume,pages[0],pages[1],"NULL","NULL","NULL", self.sourceID,filledPublication["num_citations"])
            unePublication.setDataBase(self.dataBase)
            self.publicationID = unePublication.checkIfExistsOrInsert()

            try:
                pdf_url = html_page.split('<div class="gsc_oci_title_ggi"><a href="')[1].split('"')[0]
                unDocument = Document(self.publicationID,"Publication",pdf_url, self.sourceID)
                unDocument.setDataBase(self.dataBase)
                unDocument.checkIfExistsOrInsert()
            except:
                print("No pdf found")

            unSourcePublication = SourcePublication(self.publicationID,self.sourceID,filledPublication["author_pub_id"], "NULL")
            unSourcePublication.setDataBase(self.dataBase)
            unSourcePublication.checkIfExistsOrInsert()

            unAuthorPublication = AuthorPublication(self.authorID,self.publicationID,"first")
            unAuthorPublication.setDataBase(self.dataBase)
            unAuthorPublication.checkIfExistsOrInsert()



            self.addCoAuthors(filledPublication["bib"]["author"])


    def addCoAuthors(self,coAuthors):
        authors = coAuthors.split(" and ")
        print(authors)
        for author in authors:
            unAuthor = Author("NULL",author,"NULL")
            unAuthor.setDataBase(self.dataBase)
            authorID = unAuthor.checkIfExistsOrInsert()
            
            print(author)
            
            unAuthorPublication = AuthorPublication(authorID,self.publicationID,"first")
            unAuthorPublication.setDataBase(self.dataBase)
            unAuthorPublication.checkIfExistsOrInsert()


        