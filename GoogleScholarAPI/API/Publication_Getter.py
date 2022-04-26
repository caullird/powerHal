from scholarly import scholarly
import requests
import os
from model.Publication import Publication

class Publication_Getter():

    def __init__(self, author_name):
        self.author = scholarly.fill(next(scholarly.search_author(author_name)))
        self.publications = []

    def get_pdf(self, publication, author):
        author_pub_id = publication["author_pub_id"]
        publication_filled = scholarly.fill(publication)
        user = author_pub_id.split(":")[0]
        url = "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=" + user + "&citation_for_view=" + author_pub_id
        #Page of the article
        response = requests.get(url).text
        #Scrap the url and date
        pdf_url = response.split('<div class="gsc_oci_title_ggi"><a href="')[1].split('"')[0]
        date = response.split('<div class="gsc_oci_value">')[2].split("</div>")[0]
        description = response.split('Description</div><div class="gsc_oci_value" id="gsc_oci_descr"><div class="gsh_small">  <div class="gsh_csp">')[1].split("</div")[0]
        authors = response.split('Authors</div><div class="gsc_oci_value">')[1].split("</div>")[0]
        pdf = requests.get(pdf_url)
        try:
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        except:
            os.mkdir("pdf/" + user)
            f = open("pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf", 'wb')
        f.write(pdf.content)
        f.close()

        title = publication_filled['bib']['title']
        return Publication(title, date, description,authors, "coucou", "pdf/" + user+"/" + author_pub_id.replace(":","_")+".pdf")

    def get_all_pdf(self):
        for i in self.author['publications'][0:1]:
            try:
                print(self.get_pdf(i, self.author).get_infos())
            except: 
                print("fail " + i["author_pub_id"])
        
    
pub = Publication_Getter('Sebastien Monnet')

pub.get_all_pdf()
