def can_construct_design(design, patterns, memo):
    if design in memo:
        return memo[design]
    if not design:
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern):]
            if can_construct_design(remaining, patterns, memo):
                memo[design] = True
                return True
    memo[design] = False
    return False

def count_possible_designs(patterns, designs):
    memo = {}
    count = 0
    for design in designs:
        if can_construct_design(design.strip(), patterns, memo):
            print(f"Found match for: {design}")
            count += 1
        else:
            print(f"No match for: {design}")
    return count

# Read from input file
with open('input2.txt', 'r') as file:
    # First line: patterns (comma-separated with potential spaces)
    patterns = [p.strip() for p in file.readline().strip().split(',')]
    
    # Read designs (one per line)
    designs = [line.strip() for line in file if line.strip()]

# Debug output
print(f"Number of patterns: {len(patterns)}")
print(f"Number of designs: {len(designs)}")
print("\nFirst few patterns:", patterns[:5])
print("First few designs:", designs[:5])

possible_count = count_possible_designs(patterns, designs)
print(f"\nNumber of possible designs: {possible_count}")