from model.Publication import Publication
from API.Publication_Getter import Publication_Getter
from config.DB import DB

dataBase = DB()

author = Publication_Getter('Sebastien Monnet')

author.setDataBase(dataBase)

publi = author.get_publications(4)

for i in publi:
    print('\n\n\n')
    for j in i :
        print(j)
