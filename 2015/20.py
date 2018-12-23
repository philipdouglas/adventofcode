
def adventofcode(target):
    target = target // 10
    houses = [0] * (target)
    for elf in range(1, target):
        for house in range(elf, target, elf):
            houses[house] += elf
    for index in range(1, len(houses)):
        if houses[index] > target:
            return index


def adventofcode2(target):
    target = target // 11
    houses = [0] * (target)
    for elf in range(1, target):
        visits = 0
        for house in range(elf, target, elf):
            visits += 1
            houses[house] += elf
            if visits == 50:
                break
    for index in range(1, len(houses)):
        if houses[index] > target:
            return index


if __name__ == "__main__":
    print(adventofcode(36000000))
    print(adventofcode2(36000000))
