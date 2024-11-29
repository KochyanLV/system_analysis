import json


def create_node(parent, children):
    return {
        "parent": parent,
        "children": children
    }

def process_data_recursively(current_parent, data_structure, graph):
    descendants = []
    for node_name, node_data in data_structure.items():
        if node_data:
            graph[node_name] = create_node(
                current_parent, 
                process_data_recursively(node_name, node_data, graph)
            )
        else:
            graph[node_name] = create_node(current_parent, [])
        descendants.append(node_name)
    return descendants

def convert_json_to_graph(json_data):
    graph_representation = {}
    process_data_recursively(None, json_data, graph_representation)
    return graph_representation

def display_graph_structure(graph):
    for node_name, node_info in graph.items():
        parent_node = node_info["parent"]
        siblings = [
            sibling for sibling in graph 
            if graph[sibling]["parent"] == parent_node and sibling != node_name
        ]
        children = node_info["children"]

        print(f"Узел: {node_name}")
        print(f"\tБратья: {siblings}")
        print(f"\tДети: {children}")


def main():
    with open("input.json", "r") as file:
        input_data = json.load(file)

    graph = convert_json_to_graph(input_data)
    display_graph_structure(graph)

if __name__ == "__main__":
    main()
