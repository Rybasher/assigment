import networkx as nx
import matplotlib.pyplot as plt


class Node:
    @staticmethod
    def create_tuples(nodes):
        edge_tuples = []
        for index, value in enumerate(nodes):
            if value != nodes[-1]:
                edge_tuples.append((value, nodes[index + 1]))

        print(edge_tuples)
        Edge.add_edges(edge_tuples)


class Edge:
    @staticmethod
    def add_edges(tuples):
        Graph.generate_graph(tuples)


class Graph:
    @staticmethod
    def generate_graph(tuple_list):
        g = nx.DiGraph()
        g.add_edges_from(tuple_list)
        pos = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, pos, node_size=100, node_color="blue")
        nx.draw_networkx_edges(g, pos, edgelist=g.edges(), edge_color='black', width="1")
        nx.draw_networkx_labels(g, pos, font_size="7")
        plt.rcParams["figure.figsize"] = (20, 30)

        plt.show()

