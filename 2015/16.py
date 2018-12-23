import operator

EVIDENCE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

OPERATORS = {
    'children': operator.eq,
    'cats': operator.gt,
    'samoyeds': operator.eq,
    'pomeranians': operator.lt,
    'akitas': operator.eq,
    'vizslas': operator.eq,
    'goldfish': operator.lt,
    'trees': operator.gt,
    'cars': operator.eq,
    'perfumes': operator.eq,
}

def parse_aunts(text):
    aunts = [None]
    for line in text:
        aunt = {}
        _, _, line = line.partition(': ')
        things = line.split(', ')
        for thing in things:
            item, amount = thing.split(': ')
            aunt[item] = int(amount)
        aunts.append(aunt)
    return aunts

def adventofcode():
    with open('16.txt') as input_file:
        aunts = input_file.readlines()

    aunts = parse_aunts(aunts)
    for index in range(1, len(aunts)):
        for item, value in aunts[index].items():
            if EVIDENCE[item] != value:
                break
        else:
            part1 = index
            break

    for index in range(1, len(aunts)):
        for item, value in aunts[index].items():
            if not OPERATORS[item](value, EVIDENCE[item]):
                break
        else:
            return part1, index

if __name__ == "__main__":
    print(adventofcode())
