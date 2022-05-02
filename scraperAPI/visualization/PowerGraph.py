import networkx as nx
import matplotlib.pyplot as plt

class PowerGraph():

    def __init__(self, database, author):
        self.database = database
        self.author = author
        self.authorID = self.database.getFieldsWithId(author, "Author", "display_name", "id_author", "one")
        self.graph = nx.Graph()
        self.generatePublicationCoAuthors(self.authorID)


    def generatePublicationCoAuthors(self, authorID):
        authors = []
        getPublications = self.database.getFieldsWithId(authorID, table = "AuthorPublication",searchField = "id_author", getField = "id_publication", quantity = "many")
        for publication in getPublications:
            getPublicationAuthors = self.database.getFieldsWithId(publication, table = "AuthorPublication",searchField = "id_publication", getField = "id_author", quantity = "many")
            for publicationAuthor in getPublicationAuthors:
                getAuthor = self.database.getFieldsWithId(publicationAuthor, table = "Author",searchField = "id_author", getField = "display_name", quantity = "one")
                authors.append(str(getAuthor))

        # count the number of authors in the dictionary
        authors_count = {}
        for author in authors:
            if author in authors_count:
                authors_count[author] += 1
            else:
                authors_count[author] = 1

        # fin the most author in the dictionary
        most_author = max(authors_count, key=authors_count.get)

        node_list = []
        node_size = []
        edge_list = []

        # add the authors to the graph
        for author in authors_count:
            if author != most_author:
                edge_list.append((author, most_author))
            node_list.append(author)
            node_size.append(authors_count[author]**authors_count[author]*10)

        print(node_list)
        print(node_size)

        self.graph.add_nodes_from(node_list)
        self.graph.add_edges_from(edge_list)

        nx.draw_networkx(self.graph,nodelist = node_list, node_size=node_size)

        plt.show()


