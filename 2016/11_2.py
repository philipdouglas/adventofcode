import copy

test_data = [
    {'mh', 'ml'},
    {'gh'},
    {'gl'},
    set(),
]


def is_safe(items):
    """
    >>> is_safe({'gh', 'mh'})
    True
    >>> is_safe({'gh', 'ml'})
    False
    >>> is_safe({'mh', 'ml'})
    True
    >>> is_safe({'gh', 'mh', 'mq'})
    False
    """
    radiation = False
    unprotected = False
    for item in items:
        if item[0] == 'm':
            if ('g' + item[1]) not in items:
                unprotected = True
        else:
            radiation = True
    return not unprotected or not radiation


def top_hash(items):
    """
    >>> top_hash({'mh', 'ml'}) == top_hash({'ml', 'mh'})
    True
    >>> top_hash({'gh', 'ml'}) == top_hash({'ml', 'mh'})
    True
    """
    value = 0
    for item in items:
        value &= hash(item)
    return value


def clone(bottom, top):
    return copy.copy(bottom), copy.copy(top)


def single_move(fro, to, item):
    return fro.remove(item), to.add(item)


def double_move(fro, to, items):
    fro -= items
    to |= items


def single_floor_move(bottom, top):
    top_cache = set(top)
    states = [(0, bottom, top)]
    shortest = None
    while states:
        curmoves, curbot, curtop = states.pop(0)
        print("{}:\n{}\n{}".format(curmoves, curbot, curtop))

        if not is_safe(curbot) or not is_safe(curtop):
            print("not safe")
            continue

        if len(curbot) == 0:
            shortest = curmoves
            continue

        if shortest is not None and shortest < curmoves:
            continue

        curhash = top_hash(top)
        if curhash in top_cache:
            continue
        top_cache.add(curhash)

        newmoves = curmoves + 1
        for first in [item for item in curbot if item[0] == 'm']:
            for second in curbot:
                newbot, newtop = clone(curbot, curtop)
                lift = {first, second}
                if not is_safe(lift):
                    continue
                double_move(newbot, newtop, lift)
            states.append((newmoves, newbot, newtop))

        for first in [item for item in curtop if item[0] == 'm']:
            for second in curtop:
                newbot, newtop = clone(curbot, curtop)
                lift = {first, second}
                if not is_safe(lift):
                    continue
                double_move(newtop, newbot, lift)
            states.append((newmoves, newbot, newtop))

    return shortest


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Test 1: {}".format(single_floor_move(test_data[0], test_data[1])))
