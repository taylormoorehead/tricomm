import networkx as nx
import matplotlib.pyplot as plt
import csv
import os
import math

# Create a bipartite graph
B = nx.Graph()

pharm_csv = 'NC_Pharmacies_MCM.xlsx - Feuil1.csv'
pharmacies = {}

with open(os.path.join(os.getcwd(), pharm_csv), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'NAME':
            name = row[0]
            x = row[8]
            y = row[9]

            pharmacies[name] = [x, y]

mp_csv1 = 'table01.csv'
marginal_pops_init = []

with open(os.path.join(os.getcwd(), mp_csv1), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'GEOID':
            marginal_pops_init.append(row[0])

spatial_csv = 'spatial.csv'
marginal_pops = {}

with open(os.path.join(os.getcwd(), spatial_csv), 'r') as file:
    csv_reader = csv.reader(file)

    for mp in marginal_pops_init:
        for row in csv_reader:
            if row[0] == mp:
                x = row[2]
                y = row[1]

                marginal_pops[mp] = [x, y]
                break

# Add nodes to the graph, specifying the 'bipartite' attribute
B.add_nodes_from(pharmacies.keys(), bipartite=0)  # pharmacies are in partition 0
B.add_nodes_from(marginal_pops.keys(), bipartite=1)  # marginalized populations are in partition 1

# Add edges between the two sets
edges = []
mindist = float('inf')
minpharm = ''

def distformula(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

for m in marginal_pops.keys():
    mindist = float('inf')

    for p in pharmacies.keys():
        distance = distformula(float(marginal_pops.get(m)[0]), float(marginal_pops.get(m)[1]), float(pharmacies.get(p)[0]), float(pharmacies.get(p)[1]))
        if mindist > distance:
            mindist = distance
            minpharm = p
    
    edges.append((minpharm, m))

B.add_edges_from(edges)

# Visualize the bipartite graph
pos = {node: (0, i) for i, node in enumerate(pharmacies)}  # Assign positions for the pharmacies
pos.update({node: (1, i) for i, node in enumerate(marginal_pops)})  # Assign positions for marginalized populations

plt.figure(figsize=(12, 8))

# Use a different layout algorithm (e.g., spring_layout)
pos = nx.spring_layout(B)

# Increase node size and font size
nx.draw(B, pos, with_labels=True, node_color='skyblue', node_size=50, font_size=8)

# Increase edge visibility
nx.draw_networkx_edges(B, pos, width=0.5)

# Show the plot
plt.show()