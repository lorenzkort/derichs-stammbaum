import ast
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

with open("tree.txt", "r") as f:
    content = f.read()
    family_members = ast.literal_eval(content)

# Build a dictionary for easy lookup
family_dict = defaultdict(dict)
for member in family_members:
    family_dict[member["name"]] = member

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for member in family_members:
    name = member["name"]
    parents = member["parents"]
    children = member["children"]
    partner = member["partner"]
    birth_year = member["birthYear"] if "birthYear" in member else ""
    city = member["placeOfResidency"] if "placeOfResidency" in member else ""
    occupation = member["occupation"] if "occupation" in member else ""
    generation = member["generation"] if "generation" in member else 0

    # Add person node
    G.add_node(name, birth_year=birth_year, city=city, occupation=occupation, subset=generation)

    # Add parent-child edges
    for parent in parents:
        G.add_edge(parent, name)
    for child in children:
        G.add_edge(name, child)

    # Add partner edge
    if partner:
        G.add_edge(name, partner, style="dashed")

# Position the nodes in the graph
pos = nx.multipartite_layout(G, subset_key="generation")

# Draw the graph
plt.figure(figsize=(15, 15))
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
nx.draw_networkx_edges(G, pos, width=1)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="serif")

node_labels = {}
for node in G.nodes():
    label = node + "\nBirth Year: " + G.nodes[node].get("birth_year", "") + "\nCity: " + G.nodes[node].get("city", "") + "\nOccupation: " + G.nodes[node].get("occupation", "")
    node_labels[node] = label

nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=6, font_color="black", font_family="serif", verticalalignment="center")
plt.axis("off")
plt.show()
