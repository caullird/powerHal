from scholarly import scholarly
import requests
import os
from model import Publication

class Publication_Getter():

    def __init__(self, author_name):
        self.author = scholarly.fill(next(scholarly.search_author(author_name)))
        self.publications = []

    def get_pdf(self, publication):
        author_pub_id = publication["author_pub_id"]
        publication_filled = scholarly.fill(publication)
        user = author_pub_id.split(":")[0]
        url = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=" + user + "&citation_for_view=" + author_pub_id
        #Page of the article
        response = requests.get(url).text
        #Scrap the url and date
        pdf_url = response.split('<div class="gsc_oci_title_ggi"><a href="')[1].split('"')[0]
        date = response.split('<div class="gsc_oci_value">')[2].split("</div>")[0]
        print(date)
        pdf = requests.get(pdf_url)
        try:
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        except:
            os.mkdir("pdf/" + user)
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        f.write(pdf.content)
        f.close()

        return Publication(publication_filled['bib']['title'], date, description,autheur,affiliation, pdf_lien)

    def get_all_pdf(self):
        for i in self.author['publications'][0:1]:
            try:
                self.get_pdf(i)
            except: 
                print("fail" + i["author_pub_id"])
        
    
pub = Publication_Getter('Sorana Cimpan')

pub.get_all_pdf()
