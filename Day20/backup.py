import time
from collections import deque

# Read grid from file
grid = []
with open('input3.txt', 'r') as file:
    lines = file.readlines()
    print(f"Total lines read: {len(lines)}")
    
    for line in lines:
        stripped = line.strip()
        print(f"Line length: {len(stripped)}")  # Debug line length
        if stripped:  # Skip empty lines
            grid.append(list(stripped))

# Debug: Print grid dimensions
print(f"Grid dimensions: {len(grid)}x{len(grid[0])}")

# Test print all rows to verify
print("\nFull grid:")
for row in grid:
    print(''.join(row))

def bfs(grid, start, end, ignore_wall=None):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start, 0)])
    visited = set([start])

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                new_pos = (nx, ny)
                if new_pos not in visited and (grid[ny][nx] in ('.', 'S', 'E') or new_pos == ignore_wall):
                    queue.append((new_pos, steps + 1))
                    visited.add(new_pos)

    return 0  # Return 0 if no path found

def bfs_with_two_step_cheat(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    # State: (x, y, cheatStepsLeft)
    queue = deque([(start[0], start[1], 2, 0)])  # (x, y, 2 cheat steps left, distance)
    visited = set([(start[0], start[1], 2)])

    while queue:
        x, y, cheat_left, dist = queue.popleft()
        if (x, y) == end:
            return dist

        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < cols and 0 <= ny < rows:
                cell = grid[ny][nx]
                
                # If cell is passable or it's 'S'/'E'
                if cell in ('.', 'S', 'E'):
                    # Normal move
                    if (nx, ny, cheat_left) not in visited:
                        visited.add((nx, ny, cheat_left))
                        queue.append((nx, ny, cheat_left, dist+1))

                # If cell is a wall and we still have cheat steps
                elif cell == '#' and cheat_left > 0:
                    next_cheat = cheat_left - 1
                    if (nx, ny, next_cheat) not in visited:
                        visited.add((nx, ny, next_cheat))
                        queue.append((nx, ny, next_cheat, dist+1))

    return float('inf')  # No path

def find_positions(grid):
    start = None
    end = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'S':
                start = (x, y)
            elif grid[y][x] == 'E':
                end = (x, y)
    return start, end

def find_walls(grid):
    walls = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                walls.append((x, y))
    return walls

# Find start and end coordinates
start_pos, end_pos = find_positions(grid)
walls = find_walls(grid)

# Time logging
start_time = time.time()

# Calculate initial path without removing any walls
initial_path = bfs(grid, start_pos, end_pos, None)
print(f"Initial path length: {initial_path} steps")

# Try each wall and count significant improvements
significant_shortcuts = 0
saved_steps_list = []

for wall in walls:
    path_length = bfs(grid, start_pos, end_pos, wall)
    if path_length > 0:  # Valid path found
        steps_saved = initial_path - path_length
        if steps_saved >= 100:
            significant_shortcuts += 1
            saved_steps_list.append((wall, steps_saved))

end_time = time.time()

print(f"Found {significant_shortcuts} shortcuts that save at least 100 steps")
if saved_steps_list:
    print("\nBest shortcuts:")
    # Sort by steps saved in descending order
    for wall, steps in sorted(saved_steps_list, key=lambda x: x[1], reverse=True)[:5]:
        print(f"Wall at {wall}: saves {steps} steps")

print(f"\nTotal time taken: {end_time - start_time:.4f} seconds")

normal_time = bfs_with_two_step_cheat(grid, start_pos, end_pos)