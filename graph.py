import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C')])

val_map = {
    "A": 1.00,
    "D": 0.00,
}
values = [val_map.get(nodes, 0.50) for nodes in G.nodes()]
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=values)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
nx.draw_networkx_labels(G, pos)

plt.show()