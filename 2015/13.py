import itertools
import re

regex = re.compile(
    r'([a-zA-Z]+) would (gain|lose) (\d+) happiness units by sitting next to ([a-zA-Z]+)\.')

def parse_line(line):
    """
    >>> parse_line('Alice would gain 54 happiness units by sitting next to Bob.')
    ('Alice', 'Bob', 54)
    >>> parse_line('Alice would lose 79 happiness units by sitting next to Carol.')
    ('Alice', 'Carol', -79)
    """
    match = regex.match(line)
    happiness = int(match.group(3)) * (1 if match.group(2) == 'gain' else -1)
    return match.group(1), match.group(4), happiness


def adventofcode(me=False):
    with open('13.txt') as input_file:
        lines = input_file.readlines()

    relationships = {}
    for line in lines:
        relator, relatee, happiness = parse_line(line)
        relationships.setdefault(relator, {})[relatee] = happiness
    if me:
        for relations in relationships.values():
            relations['Me'] = 0
        relationships['Me'] = {person: 0 for person in relationships.keys()}

    layouts = itertools.permutations(relationships.keys())

    best = 0
    for layout in layouts:
        happiness = 0
        previous_person = layout[-1]
        for current_person in layout:
            happiness += relationships[previous_person][current_person]
            happiness += relationships[current_person][previous_person]
            previous_person = current_person
        best = max(best, happiness)
    return best


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
    print(adventofcode(True))
