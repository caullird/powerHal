import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from bokeh.plotting import figure, show, output_file, from_networkx
from bokeh.models import (
    BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.palettes import Spectral4
import io

from config.DB import DB

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from flask import Response

class PowerGraph():

    def __init__(self, research):
        self.database = DB()
        self.database.setConnectedUserId(research['id_connected_user']) 
        self.authorID = research['id_author_as_user']
        self.graph = nx.Graph()

    def generatePublicationCoAuthors(self):
        authors = []
        getPublications = self.database.getFieldsWithId(self.authorID, table = "AuthorPublication",searchField = "id_author", getField = "id_publication", quantity = "many")
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


        top_autors = {}

        if len(authors_count)< 15:
            top_autors = authors_count
        else:
            for i in range(15):
                max_author = max(authors_count, key=authors_count.get)
                top_autors[max_author] = authors_count[max_author]
                authors_count[max_author] = 0


        # fin the most author in the dictionary
        most_author = max(top_autors, key=top_autors.get)

        node_list = []
        node_size_list = []
        edge_list = []
        edge_size = []
        edge_labels = {}

        # add the authors to the graph
        for author in top_autors:
            if author != most_author:
                edge_list.append((author, most_author))
                edge_size.append(top_autors[author])
                edge_labels[(author, most_author)] = top_autors[author]
            node_list.append(author)
            #node_size.append(top_autors[author])
            node_size_list.append(len(author)*600)

        print(node_list)

        self.graph.add_nodes_from(node_list)
        self.graph.add_edges_from(edge_list)

        blue = plt.cm.get_cmap('Blues')
        print(blue)
        blue_trunc = colors.LinearSegmentedColormap.from_list(
            'trunc({n},{a:.2f},{b:.2f})'.format(n=blue.name, a=0.5, b=1),
            blue(np.linspace(0.5, 1, 100)))

        fig = plt.figure(1, figsize=(20,12))

        fig.clear()

        pos = nx.spring_layout(self.graph)
        
        # draw the graph
        nodes = nx.draw_networkx_nodes(self.graph, pos, node_color='white', node_size=node_size_list)
        edges = nx.draw_networkx_edges(self.graph, pos, edge_color=edge_size, width=10.0, edge_cmap=blue_trunc)
        
        nx.draw_networkx_labels(self.graph, pos, font_size=11)
        nx.draw_networkx_edge_labels(self.graph,pos,edge_labels=edge_labels,font_color='black', font_size=20, rotate=False)
        
        nodes.set_edgecolor('black')


        return fig



