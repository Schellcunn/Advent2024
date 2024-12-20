from collections import deque


file_name = "input.txt"
# Example input
byte_positions = []
with open(file_name, 'r') as file:
    for line in file:
        x, y = map(int, line.strip().split(','))  # Split by ',' and convert to integers
        byte_positions.append((x, y))

print(byte_positions)
grid_size = 71 


# Initialize the grid
grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]

# Simulate falling bytes
for i, (x, y) in enumerate(byte_positions[:1024]):  # Limit to the first 1024 bytes
    grid[y][x] = '#'

# Define BFS to find the shortest path
def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
    queue = deque([(start, 0)])  # (position, steps)
    visited = set([start])

    while queue:
        (x, y), steps = queue.popleft()

        # Check if we reached the target
        if (x, y) == end:
            return steps

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited and grid[ny][nx] == '.':
                queue.append(((nx, ny), steps + 1))
                visited.add((nx, ny))

    return float('inf')  # No path found

# Start and end points
start = (0, 0)
end = (grid_size - 1, grid_size - 1)

# Compute the shortest path
shortest_path = bfs(grid, start, end)

# Output the grid and the result
print("\nMemory Space After Corruption:")
for row in grid:
    print(''.join(row))

if shortest_path != float('inf'):
    print(f"\nMinimum steps to reach the exit: {shortest_path}")
else:
    print("\nNo path to the exit found!")
