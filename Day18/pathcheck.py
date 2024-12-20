# Read byte positions from file
file_name = 'input.txt'
byte_positions = []
with open(file_name, 'r') as file:
    for line in file:
        x, y = map(int, line.strip().split(','))
        byte_positions.append((x, y))

# Determine the required grid size
max_x = max(x for x, y in byte_positions)
max_y = max(y for x, y in byte_positions)
grid_size_x = max_x + 1  # Add 1 because coordinates are 0-indexed
grid_size_y = max_y + 1

# Initialize grid
grid = [['.' for _ in range(grid_size_x)] for _ in range(grid_size_y)]

# Start and end positions
start = (0, 0)
end = (grid_size_x - 1, grid_size_y - 1)

# Function to check if a path exists using BFS
from collections import deque

def is_path_available(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([start])
    visited = set([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited and grid[ny][nx] == '.':
                queue.append((nx, ny))
                visited.add((nx, ny))

    return False

# Simulate byte falling and check for the blocking byte
for i, (x, y) in enumerate(byte_positions):
    grid[y][x] = '#'  # Mark the byte position as corrupted
    if not is_path_available(grid, start, end):
        print(f"{x},{y}")  # Output the blocking byte's coordinates
        break
