from collections import defaultdict

def parse_data(my_file) -> list:
    with open(my_file) as f:
        return [int(num) for num in f.readlines()]

def mix_prune(secret:int, num:int) -> int:
    return (secret ^ num) % 16777216

def part1(data:list) -> int:
    total = 0
    changes4 = defaultdict(list)
    for x in data:
        prev = x % 10
        change = (prev,)
        first = set()
        for _ in range(2000):
            x = mix_prune(x, x * 64)
            x = mix_prune(x, x // 32)
            x = mix_prune(x, x * 2048)
            last = x % 10
            if len(change) > 3:
                change = change[1:] + (last - prev,)
                if change not in first:
                    changes4[change].append(last)
                    first.add(change)
            else:
                change += (last - prev,)
            prev = last
        total += x
    return total, max(sum(nums) for nums in changes4.values())

# Read data from debug.txt
data = parse_data('input5.txt')
p1 = part1(data)
print('Part 1: ', p1[0])
print('Part 2: ', p1[1])