from scholarly import scholarly
import requests
import os
from model.Publication import Publication

class Publication_Getter():

    def __init__(self, author_name):
        self.author = scholarly.fill(next(scholarly.search_author(author_name)))
        self.publications = []

    # Get the info about one publication
    def get_publication(self, publication, publication_result):
        author_pub_id = publication["author_pub_id"]
        publication_filled = scholarly.fill(publication)
        user = author_pub_id.split(":")[0]
        url = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=" + user + "&citation_for_view=" + author_pub_id
        #Page of the article
        response = requests.get(url).text
        #Scrap the url and date
        pdf_url = response.split('<div class="gsc_oci_title_ggi"><a href="')[1].split('"')[0]
        pdf = requests.get(pdf_url)
        try:
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        except:
            os.mkdir("pdf/" + user)
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        f.write(pdf.content)
        f.close()

        title = publication_filled['bib']['title']
        date = response.split('<div class="gsc_oci_value">')[2].split("</div>")[0]
        description = publication_filled['bib']['abstract']
        authors = publication_filled['bib']['author']

        publication_result.set_infos(title, date, description, authors, "", "pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf")
        publication_result.database.checkIfExistsOrInsert(publication_result, fieldsComparable = ['id_scholar'])
        return publication_result

    # Get all the publications info and return a list
    def get_publications(self, max):
        if max > len(self.author['publications']):
            max = len(self.author['publications'])
        for publication in self.author['publications'][0:max]:
            pub_id = publication['author_pub_id'].split(":")[1]
            if not self.database.checkIfPublicationExists(pub_id):
                print("je n'existe pas")
                try:
                    self.publications.append(self.get_publication(publication, Publication(self.database, pub_id)).get_infos())
                except: 
                    print("fail " + publication["author_pub_id"])
            else :
                print("je existe")
        return self.publications

    # Permet d'ajouter l'objet database à l'objet Publication
    def setDataBase(self, database):
        self.database = database
        
    



