from flask import Flask, request, render_template, jsonify
import networkx as nx
from keybert import KeyBERT
from itertools import permutations
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Create a graph representing the supermarket layout
G = nx.Graph()

# Define nodes and their positions
nodes = {
    'Entrance': (0, 0),
    'Aisle 1': (1, 0),
    'Aisle 2': (2, 0),
    'Aisle 3': (3, 0),
    'Aisle 4': (4, 0),
    'Aisle 5': (5, 0),
    'Dairy': (1, 1),
    'Bakery': (2, 1),
    'Produce': (3, 1),
    'Meat': (4, 1),
    'Frozen': (5, 1),
    'Snacks': (1, 2),
    'Beverages': (2, 2),
    'Household': (3, 2),
    'Personal Care': (4, 2),
    'Checkout': (5, 2),
    'Corner 1': (1, -1),
    'Corner 2': (2, -1),
    'Corner 3': (3, -1),
    'Corner 4': (4, -1),
    'Corner 5': (5, -1),
    'Corner 6': (1, 3),
    'Corner 7': (2, 3),
    'Corner 8': (3, 3),
    'Corner 9': (4, 3),
    'Corner 10': (5, 3)
}

# Add nodes to the graph
for node, pos in nodes.items():
    G.add_node(node, pos=pos)

# Add edges with distances
edges = [
    ('Entrance', 'Aisle 1', 1),
    ('Aisle 1', 'Aisle 2', 1),
    ('Aisle 2', 'Aisle 3', 1),
    ('Aisle 3', 'Aisle 4', 1),
    ('Aisle 4', 'Aisle 5', 1),
    ('Aisle 1', 'Dairy', 1),
    ('Aisle 2', 'Bakery', 1),
    ('Aisle 3', 'Produce', 1),
    ('Aisle 4', 'Meat', 1),
    ('Aisle 5', 'Frozen', 1),
    ('Dairy', 'Snacks', 1),
    ('Bakery', 'Beverages', 1),
    ('Produce', 'Household', 1),
    ('Meat', 'Personal Care', 1),
    ('Frozen', 'Checkout', 1),
    ('Corner 1', 'Dairy', 1),
    ('Corner 2', 'Bakery', 1),
    ('Corner 3', 'Produce', 1),
    ('Corner 4', 'Meat', 1),
    ('Corner 5', 'Frozen', 1),
    ('Corner 1', 'Corner 2', 1),
    ('Corner 2', 'Corner 3', 1),
    ('Corner 3', 'Corner 4', 1),
    ('Corner 4', 'Corner 5', 1),
    ('Corner 6', 'Snacks', 1),
    ('Corner 7', 'Beverages', 1),
    ('Corner 8', 'Household', 1),
    ('Corner 9', 'Personal Care', 1),
    ('Corner 10', 'Checkout', 1),
    ('Corner 6', 'Corner 7', 1),
    ('Corner 7', 'Corner 8', 1),
    ('Corner 8', 'Corner 9', 1),
    ('Corner 9', 'Corner 10', 1)
]

for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Initialize KeyBERT model
kw_model = KeyBERT()

# Improved item location mapping with more comprehensive data
item_locations = {
    'milk': 'Dairy',
    'bread': 'Bakery',
    'apple': 'Produce',
    'chicken': 'Meat',
    'ice cream': 'Frozen',
    'chips': 'Snacks',
    'soda': 'Beverages',
    'detergent': 'Household',
    'shampoo': 'Personal Care',
    # Add more items and their locations
    'butter': 'Dairy',
    'cake': 'Bakery',
    'banana': 'Produce',
    'beef': 'Meat',
    'frozen pizza': 'Frozen',
    'cookies': 'Snacks',
    'juice': 'Beverages',
    'cleaner': 'Household',
    'toothpaste': 'Personal Care'
}


def get_item_location(item_name):
    return item_locations.get(item_name.lower(), 'Unknown')


def predict_item_names(input_text):
    # Use KeyBERT to extract keywords
    keywords = kw_model.extract_keywords(input_text, keyphrase_ngram_range=(1, 1), stop_words=None)
    item_names = [kw[0] for kw in keywords if kw[0] in item_locations]
    return item_names


def find_shortest_path(graph, start, end):
    return nx.shortest_path(graph, source=start, target=end, weight='weight')


def find_shortest_path_multiple(graph, start, items):
    min_path = None
    min_distance = float('inf')

    for perm in permutations(items):
        current_distance = 0
        current_path = [start]

        for i in range(len(perm)):
            if i == 0:
                partial_path = find_shortest_path(graph, start, perm[i])
            else:
                partial_path = find_shortest_path(graph, perm[i - 1], perm[i])
                partial_path = partial_path[1:]  # Avoid duplicating nodes
            current_path.extend(partial_path)
            current_distance += sum(nx.dijkstra_path_length(graph, partial_path[j], partial_path[j + 1]) for j in
                                    range(len(partial_path) - 1))

        if current_distance < min_distance:
            min_distance = current_distance
            min_path = current_path

    # Remove duplicate 'Entrance' if it appears more than once
    if min_path and min_path[0] == start and min_path[1] == start:
        min_path = min_path[1:]

    # Add the path to the checkout from the last item
    checkout_path = find_shortest_path(graph, min_path[-1], 'Checkout')
    min_path.extend(checkout_path[1:])  # Skip the starting node to avoid duplication

    return min_path, min_distance


def visualize_path(graph, pos, path, title):
    path_edges = list(zip(path, path[1:]))
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold',
            edge_color='lightgray', width=2)
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', arrows=True)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))
    plt.title(title)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find_path', methods=['POST'])
def find_path():
    input_text = request.form['items']
    item_names = predict_item_names(input_text)
    item_locations_list = [get_item_location(item) for item in item_names]

    if 'Unknown' not in item_locations_list:
        shortest_path, _ = find_shortest_path_multiple(G, 'Entrance', item_locations_list)
        plot_url = visualize_path(G, nx.get_node_attributes(G, 'pos'), shortest_path, f'Shortest Path to {item_names}')
        # Generate the text representation of the path
        path_text = ' -> '.join(shortest_path)
        return render_template('result.html', item_names=item_names, plot_url=plot_url, path_text=path_text)
    else:
        return 'One or more items not found', 400


if __name__ == '__main__':
    app.run(debug=True)
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
