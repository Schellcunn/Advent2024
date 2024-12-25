import sys
from enum import Enum
from functools import cache
from typing import NamedTuple, Iterator, List, Dict, Set, Tuple
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Position:
    x: int
    y: int


NUMPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [" ", "0", "A"],
]

NUMPAD_POSITIONS = {char: Position(x, y) for y, row in enumerate(NUMPAD) for x, char in enumerate(row)}


DIRPAD = [
    [" ", "^", "A"],
    ["<", "v", ">"],
]

DIRPAD_POSITIONS = {char: Position(x, y) for y, row in enumerate(DIRPAD) for x, char in enumerate(row)}


class KeypadType(Enum):
    NUMPAD = 0
    DIRPAD = 1

    def key_positions(self):
        return NUMPAD_POSITIONS if self == KeypadType.NUMPAD else DIRPAD_POSITIONS


@cache
def find_shortest_sequence(code: str, proxies: int, keypad_type: KeypadType = KeypadType.NUMPAD) -> int:
    sequences = keypad_control_sequences(code, keypad_type)
    if proxies == 0:
        return min(sum(len(part) for part in sequence) for sequence in sequences)
    else:
        return min(sum(find_shortest_sequence(dircode, proxies - 1, KeypadType.DIRPAD) for dircode in sequence) for sequence in sequences)


def keypad_control_sequences(code: str, keypad_type: KeypadType, start: str = "A") -> list[list[str]]:
    if code == "":
        return [[]]
    keypad_positions = keypad_type.key_positions()
    position = keypad_positions[start]
    next_position = keypad_positions[code[0]]
    gap = keypad_positions[" "]

    return [
        [option, *sequence]
        for sequence in keypad_control_sequences(code[1:], keypad_type, start=code[0])
        for option in get_move_options(position, next_position, gap)
    ]


def get_move_options(position: Position, next_position: Position, gap: Position) -> Iterator[str]:
    horizontal_arrow = "<" if next_position.x < position.x else ">"
    vertical_arrow = "^" if next_position.y < position.y else "v"
    horizontal_distance = abs(position.x - next_position.x)
    vertical_distance = abs(position.y - next_position.y)
    if position == next_position:
        yield "A"
    elif position.x == next_position.x:
        yield vertical_arrow * vertical_distance + "A"
    elif position.y == next_position.y:
        yield horizontal_arrow * horizontal_distance + "A"
    else:
        if not (
            (gap.x == next_position.x and gap.y in nonempty_range(position.y, next_position.y))
            or (gap.y == position.y and gap.x in nonempty_range(next_position.x, position.x))
        ):
            yield horizontal_arrow * horizontal_distance + vertical_arrow * vertical_distance + "A"
        if not (
            (gap.x == position.x and gap.y in nonempty_range(next_position.y, position.y))
            or (gap.y == next_position.y and gap.x in nonempty_range(position.x, next_position.x))
        ):
            yield vertical_arrow * vertical_distance + horizontal_arrow * horizontal_distance + "A"


def nonempty_range(start, end) -> range:
    assert start != end
    if start < end:
        return range(start, end)
    else:
        return range(start, end, -1)


class KeypadSolver:
    def __init__(self):
        self.numeric_layout = {
            Position(0,0):'7', Position(0,1):'8', Position(0,2):'9',
            Position(1,0):'4', Position(1,1):'5', Position(1,2):'6',
            Position(2,0):'1', Position(2,1):'2', Position(2,2):'3',
            Position(3,1):'0', Position(3,2):'A'
        }
        self.start_pos = Position(3, 2)  # Start at 'A'

    def find_path(self, target: str) -> str:
        visited = set()
        queue = deque([(self.start_pos, "")])
        
        while queue:
            pos, path = queue.popleft()
            if self.numeric_layout[pos] == target:
                return path + "A"
            
            for next_pos, move in self.get_valid_moves(pos):
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + move))
        return ""

    def get_valid_moves(self, pos: Position) -> List[Tuple[Position, str]]:
        moves = []
        directions = [
            (0,1,">"), (0,-1,"<"),
            (-1,0,"^"), (1,0,"v")
        ]
        
        for dx, dy, direction in directions:
            new_pos = Position(pos.x + dx, pos.y + dy)
            if new_pos in self.numeric_layout:
                moves.append((new_pos, direction))
        return moves

    def solve_code(self, code: str) -> str:
        current = self.start_pos
        sequence = ""
        
        for digit in code:
            path = self.find_path(digit)
            sequence += path
            current = next(pos for pos, val in self.numeric_layout.items() 
                         if val == digit)
            self.start_pos = current
            
        return sequence


def calculate_complexity(code: str, sequence: str) -> int:
    numeric_part = int(code.replace('A', '').lstrip('0') or '0')
    return len(sequence) * numeric_part


def main():
    with open('input4.txt', 'r') as f:
        codes = [line.strip() for line in f]
    
    solver = KeypadSolver()
    total = 0
    
    for code in codes:
        sequence = solver.solve_code(code)
        complexity = calculate_complexity(code, sequence)
        total += complexity
        print(f"Code: {code}")
        print(f"Sequence: {sequence}")
        print(f"Complexity: {complexity}")
    
    print(f"Total complexity: {total}")


if __name__ == "__main__":
    main()