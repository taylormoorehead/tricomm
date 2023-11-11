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

mp_csv1 = 'table11.csv'
marginal_pops_init = {}

with open(os.path.join(os.getcwd(), mp_csv1), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'GEOID':
            marginal_pops_init[row[0]] = [row[1], row[2]]

spatial_csv = 'spatial.csv'
marginal_pops = {}

with open(os.path.join(os.getcwd(), spatial_csv), 'r') as file:
    csv_reader = csv.reader(file)

    for mp in marginal_pops_init.keys():
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
    
    edges.append((minpharm, m, mindist))

minpop = ''

for p in pharmacies.keys():
    mindist = float('inf')

    if not edges.__contains__(p):
        for m in marginal_pops.keys():
            distance = distformula(float(marginal_pops.get(m)[0]), float(marginal_pops.get(m)[1]), float(pharmacies.get(p)[0]), float(pharmacies.get(p)[1]))
            if mindist > distance:
                mindist = distance
                minpop = m
    
        edges.append((p, minpop, mindist))

B.add_weighted_edges_from(edges)

csv_lines = {}

for p in pharmacies:
    adj_mp = []

    for e in edges:
        if p in e:
            # Determine the other node connected to 'p' in the edge 'e'
            adj_node = e[0] if e[1] == p else e[1]
            adj_mp.append(adj_node)

    total_pop = 0
    demo_pop = 0

    for a in adj_mp:
        total_pop += float(marginal_pops_init.get(a)[0])
        demo_pop += float(marginal_pops_init.get(a)[1])

    if not total_pop == 0:
        csv_lines[p] = [[adj_mp], [float(demo_pop / total_pop)]]
    else:
        csv_lines[p] = [[adj_mp], [float(0)]]

output_csv = 'stats11.csv'

with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the headers
    csv_writer.writerow(['Pharmacy', 'Populations', 'Percent'])

    # Write the rows
    for pharmacy, values in csv_lines.items():
        # Unpack values list
        population, percent = values

        csv_writer.writerow([pharmacy, population, percent])

print("CSV file has been successfully created.")

# # Visualize the bipartite graph
# pos = {node: (0, i) for i, node in enumerate(pharmacies)}  # Assign positions for the pharmacies
# pos.update({node: (1, i) for i, node in enumerate(marginal_pops)})  # Assign positions for marginalized populations

# plt.figure(figsize=(12, 8))

# # Use a different layout algorithm (e.g., spring_layout)
# pos = nx.spring_layout(B)

# # Increase node size and font size
# nx.draw(B, pos, with_labels=True, node_color='skyblue', node_size=50, font_size=8)

# # Increase edge visibility
# nx.draw_networkx_edges(B, pos, width=[d['weight'] for (u, v, d) in B.edges(data=True)], edge_color='gray')

# # Show the plot
# plt.show()