import networkx as nx
import matplotlib.pyplot as plt

# Create a bipartite graph
B = nx.Graph()

# Define nodes for two sets (e.g., pharmacies and marginalized populations)
pdict = {'P1': 0, 'P2': 1, 'P3': 2}
mpdict = {'M1': 0, 'M2': 2, 'M3': 1}

pharmacies = list(pdict.keys())
marginalized_populations = list(mpdict.keys())

# Add nodes to the graph, specifying the 'bipartite' attribute
B.add_nodes_from(pdict.keys(), bipartite=0)  # pharmacies are in partition 0
B.add_nodes_from(mpdict.keys(), bipartite=1)  # marginalized populations are in partition 1

# Add edges between the two sets
edges = []

for p in pdict.keys():
    for m in mpdict.keys():
        if pdict.get(p) == mpdict.get(m):
            edges.append([p, m])

B.add_edges_from(edges)

# Visualize the bipartite graph
pos = {node: (0, i) for i, node in enumerate(pharmacies)}  # Assign positions for the pharmacies
pos.update({node: (1, i) for i, node in enumerate(marginalized_populations)})  # Assign positions for marginalized populations

nx.draw(B, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=8)
plt.show()
