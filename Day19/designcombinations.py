def count_combinations(design, patterns, memo=None):
    if memo is None:
        memo = {}
    if design in memo:
        return memo[design]
    if not design:
        return 1
    
    total = 0
    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern):]
            total += count_combinations(remaining, patterns, memo)
    
    memo[design] = total
    return total

def sum_all_combinations(patterns, designs):
    total = 0
    for design in designs:
        combinations = count_combinations(design.strip(), patterns)
        if combinations > 0:
            print(f"Design {design}: {combinations} combinations")
        total += combinations
    return total

# Read input
with open('input2.txt', 'r') as file:
    patterns = [p.strip() for p in file.readline().strip().split(',')]
    designs = [line.strip() for line in file if line.strip()]

# Get total combinations
total = sum_all_combinations(patterns, designs)
print(f"\nTotal possible combinations: {total}")