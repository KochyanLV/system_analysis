import json
from math import log2

def create_graph_node(parent_node, child_nodes):
    return {
        "parent": parent_node,
        "children": child_nodes
    }

def build_graph_recursively(parent_node, input_data, graph_structure):
    child_keys = []
    for node_name, node_children in input_data.items():
        if node_children:
            graph_structure[node_name] = create_graph_node(
                parent_node, 
                build_graph_recursively(node_name, node_children, graph_structure)
            )
        else:
            graph_structure[node_name] = create_graph_node(parent_node, [])
        child_keys.append(node_name)
    return child_keys

def parse_json_to_graph(json_data):
    graph = {}
    build_graph_recursively(None, json_data, graph)
    return graph

def find_peers(graph, node_name):
    node_parent = graph[node_name]["parent"]
    return [
        sibling_name for sibling_name in graph 
        if graph[sibling_name]["parent"] == node_parent and sibling_name != node_name
    ]

def count_parent_levels(node_name, graph):
    current_node = node_name
    level_count = 0
    while graph[current_node]["parent"] is not None:
        level_count += 1
        current_node = graph[current_node]["parent"]
    return level_count

def count_all_descendants(graph, child_list, counter):
    if not child_list:
        return
    for child_name in child_list:
        count_all_descendants(graph, graph[child_name]["children"], counter)
        counter.value += 1

class Counter:
    def __init__(self):
        self.value = 0

def analyze_relationships(graph):
    results = [[0 for _ in range(len(graph))] for _ in range(5)]
    for node_name, node_info in graph.items():
        node_index = int(node_name) - 1
        results[0][node_index] = 1 if node_info["parent"] else 0 
        results[1][node_index] = len(node_info["children"]) 
        results[2][node_index] = count_parent_levels(node_name, graph) - 1 if node_info["parent"] else 0  
        peers = find_peers(graph, node_name)
        descendant_counter = Counter()
        for child in node_info["children"]:
            count_all_descendants(graph, graph[child]["children"], descendant_counter)
        results[3][node_index] = descendant_counter.value
        results[4][node_index] = len(peers) 
    
    return results

def entropy(matrix):
    n = len(matrix[0]) - 1
    return sum(
        -sum((elem / n) * log2(elem / n) for elem in column if elem != 0)
        for column in zip(*matrix)
    )


def main():
    with open("input.json", "r") as file:
        json_data = json.load(file)
    graph_structure = parse_json_to_graph(json_data)
    matrix = analyze_relationships(graph_structure)

    print(f"Энтропия равна: {entropy(matrix):.2f}")

if __name__ == "__main__":
    main()