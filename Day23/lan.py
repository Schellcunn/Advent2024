file_name = 'input6.txt'
connections = []
with open(file_name, 'r') as file:
    for line in file:
        x = line.strip().split('-')
        connections.append(x)

# Create a graph from the connections
graph = {}
for conn in connections:
    a, b = conn
    if a not in graph:
        graph[a] = []
    if b not in graph:
        graph[b] = []
    graph[a].append(b)
    graph[b].append(a)

# Function to find all groups of three interconnected computers
def find_groups_of_three(graph):
    groups = set()
    for node in graph:
        for neighbor in graph[node]:
            for second_neighbor in graph[neighbor]:
                if second_neighbor in graph[node] and node != second_neighbor:
                    group = tuple(sorted([node, neighbor, second_neighbor]))
                    groups.add(group)
    return groups

# Find and print the groups of three interconnected computers
groups_of_three = find_groups_of_three(graph)
count_with_t = 0
for group in groups_of_three:
    print(','.join(group))
    if any(computer.startswith('t') for computer in group):
        count_with_t += 1

print(f"Number of groups containing at least one computer with a name that starts with 't': {count_with_t}")
