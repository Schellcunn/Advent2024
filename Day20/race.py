import time
from collections import deque

START = "S"
END = "E"
WALL = "#"


def inWorld(row:int,col:int,track:list[list[str]]):
    return 0 <= row < len(track) and 0 <= col < len(track[row])

def bfs(track:list[list[str]], start:tuple[int,int], end:tuple[int,int]):
    """
    BFS to return one path from start to end (list of (row,col) positions).
    If no path found, returns an empty list.
    """
    from collections import deque
    queue = deque()
    queue.append(start)
    visited = {start}
    parent = {start: None}  # Track predecessors for path reconstruction

    while queue:
        row, col = queue.popleft()
        if (row, col) == end:
            # Reconstruct path from end to start
            path = []
            cur = end
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]  # Reverse it to go from start -> end
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = row + dr, col + dc
            if not inWorld(nr, nc, track):
                continue
            if track[nr][nc] == WALL:
                continue
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (row, col)
                queue.append((nr, nc))
    return []

def getCheats(path:list[tuple[int,int]], maxCheats:int, threshold:int):
    """
    path: BFS-discovered path from S -> E as [(r,c), (r,c), ...].
    maxCheats: max distance to 'skip' with cheat
    threshold: required amount of time saved
    """
    raceTime = len(path) - 1  # total steps
    count = 0
    for i in range(len(path)-1):
        for j in range(i+1, len(path)):
            posA, posB = path[i], path[j]
            distance = abs(posA[0] - posB[0]) + abs(posA[1] - posB[1])
            if distance > maxCheats:
                continue
            cheatTime = (i + 1) + distance + (raceTime - j - 1)
            timeSaved = raceTime - cheatTime
            if timeSaved >= threshold:
                count += 1
    print(count)

def getTrack(fileName:str):
    with open(fileName, 'r') as file:
        track = []
        start = (0,0)
        end = (0,0)
        for i, line in enumerate(file):
            rowData = line.strip()
            if not rowData:
                continue
            curRow = []
            for j, ch in enumerate(rowData):
                curRow.append(ch)
                if ch == END:
                    end = (i,j)
                elif ch == START:
                    start = (i,j)
            track.append(curRow)
        return track, start, end

def getBestCheatCounts(fileName:str, maxCheats:int, threshold:int):
    track, start, end = getTrack(fileName)
    path = bfs(track, start, end)
    if not path:
        print(f"No path found in {fileName}.")
    else:
        getCheats(path, maxCheats, threshold)

def main():
    # Single test with input3.txt
    print("Processing input3.txt...")
    getBestCheatCounts("input3.txt", 2, 100)

if __name__ == "__main__":
    main()