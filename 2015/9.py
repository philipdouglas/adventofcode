import itertools
import re

regex = re.compile(r'([a-zA-Z]+) to ([a-zA-Z]+) = (\d+)')


def adventofcode():
    with open('9.txt') as input_file:
        paths = input_file.readlines()

    places = {}
    for path in paths:
        match = regex.match(path)
        place1 = match.group(1)
        place2 = match.group(2)
        distance = int(match.group(3))

        places.setdefault(place1, {})[place2] = distance
        places.setdefault(place2, {})[place1] = distance

    routes = itertools.permutations(places.keys())
    shortest = None
    longest = 0
    for route in routes:
        length = 0
        last_place = None
        for place in route:
            if last_place is None:
                last_place = place
                continue
            length += places[last_place][place]
            last_place = place
        if shortest is None or length < shortest:
            shortest = length
        if length > longest:
            longest = length
    return shortest, longest


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
