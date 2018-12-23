import copy


class Irradiated(Exception):
    pass


class Base:
    def __init__(self, element):
        self.element = element

    def __eq__(self, other):
        """
        >>> Gen('lithium') == Gen('lithium')
        True
        >>> Gen('lithium') == Chip('lithium')
        False
        """
        return (
            isinstance(other, self.__class__) and
            self.element == other.element
        )

    def __hash__(self):
        return hash(self.__class__) ^ hash(self.element)

    def __deepcopy__(self, memo):
        return self


class Gen(Base):
    letter = 'G'


NULL = Gen(None)


class Chip(Base):
    letter = 'M'


class State:
    def __init__(self, floors, lift_floor=0):
        self.floors = floors
        self.total_items = sum(len(floor) for floor in self.floors)
        self.lift_floor = lift_floor
        self.moves = 0
        self.success = False

    def __eq__(self, oth):
        return self.lift_floor == oth.lift_floor and self.floors == oth.floors

    def __hash__(self):
        """
        >>> hash(State([[Gen('a')], [Chip('b')]])) != hash(State([[Gen('a'), Chip('b')]]))
        True
        """
        value = 0
        for index in range(len(self.floors)):
            floor = [str(item) for item in self.floors[index]]
            floor = str(index) + ''.join(sorted(floor))
            value ^= hash(floor)
        return value ^ hash(str(self.lift_floor))

    def check_state(self):
        """
        >>> state = State([[], [], []])
        >>> state.check_state()
        True
        >>> State([[Gen('a')], [Chip('b')]]).check_state()
        False
        >>> State([[Gen('h'), Chip('h'), Gen('l')]]).check_state()
        True
        >>> State([[Gen('b'), Chip('b')]]).check_state()
        True
        >>> State([[Gen('h'), Chip('t'), Gen('l')]]).check_state()
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        Irradiated
        >>> State([[Chip('a'), Chip('b')], [Gen('a')], [Gen('b')]]).check_state()
        False
        >>> State([[Chip('b')], [Chip('a'), Gen('a')], [Gen('b')]]).check_state()
        False
        >>> State([[Chip('b')], [], [Chip('a'), Gen('a'), Gen('b')]]).check_state()
        False
        """
        for floor in self.floors:
            chips = {chip.element for chip in floor if isinstance(chip, Chip)}
            gens = {gen.element for gen in floor if isinstance(gen, Gen)}
            irradiated = len(gens)
            unprotected = False
            for chip in chips:
                if chip not in gens:
                    unprotected = True
            if irradiated and unprotected:
                raise Irradiated
        if len(self.floors[-1]) == self.total_items:
            return True
        return False

    def remove_items(self, floor, items):
        for item in items:
            self.floors[floor].remove(item)

    def add_items(self, floor, items):
        self.floors[floor] += items

    def bottom_active_floor(self):
        for index in range(0, self.lift_floor):
            if self.floors[index]:
                return False
        return True

    def next_steps(self):
        routes = []
        if (self.lift_floor + 1) < len(self.floors):
            routes.append(1)
        if self.lift_floor > 0 and not self.bottom_active_floor():
            routes.append(-1)

        options = set()
        for item in self.floors[self.lift_floor]:
            for other_item in self.floors[self.lift_floor]:
                options.add(tuple({item, other_item}))

        options = sorted(options, key=lambda opt: len(opt), reverse=True)
        for direction in routes:
            new_floor = self.lift_floor + direction
            if new_floor < 0 or new_floor >= len(self.floors):
                continue
            valid_pair = False
            for option in options:
                # if len(option) == 1 and valid_pair:
                #     break
                try:
                    new_state = copy.deepcopy(self)
                    new_state.moves += 1
                    # print(new_state.moves)
                    new_state.remove_items(self.lift_floor, option)
                    new_state.add_items(new_floor, option)
                    new_state.lift_floor = new_floor
                    if new_state.check_state():
                        new_state.success = True
                    if len(option) == 2:
                        valid_pair = True
                    yield new_state
                except Irradiated:
                    # print('irradiated: {}'.format(new_state.simplify()))
                    continue

    def simplify(self):
        """
        >>> state = State([[Gen('1'), Chip('2')], [Gen('2')], [Chip('1')]])
        >>> state.simplify()
        (0, ((0, 1), (2, 0)))
        >>> state = State([[Gen('2'), Chip('1')], [Gen('1')], [Chip('2')]])
        >>> state.simplify()
        (0, ((0, 1), (2, 0)))
        """
        chips = {}
        generators = {}
        for index in range(len(self.floors)):
            for item in self.floors[index]:
                if isinstance(item, Gen):
                    generators[item.element] = index
                else:
                    chips[item.element] = index
        pairs = list()
        for element, chipfloor in chips.items():
            pairs.append((chipfloor, generators[element]))
        return (
            self.lift_floor, tuple(sorted(pairs)))

    def __str__(self):
        string = ''
        for floor_number in range(len(self.floors)):
            string += str(self.floors[floor_number]) + (' E\n' if floor_number == self.lift_floor else '\n')
        return string

    def top_heavyness(self):
        return len(self.floors[-1]) * 10 + len(self.floors[-2]) * 5


test_data = [
    [Chip('hydrogen'), Chip('lithium')],
    [Gen('hydrogen')],
    [Gen('lithium')],
    [],
]

easy_mode = [
    [Chip('hydrogen'), Gen('lithium'), Gen('hydrogen'), Chip('lithium')],
    [],
]

part1 = [
    [Gen('strontium'), Chip('strontium'), Gen('plutonium'), Chip('plutonium')],
    [Gen('thulium'), Gen('ruthenium'), Chip('ruthenium'), Gen('curium'), Chip('curium')],
    [Chip('thulium')],
    [],
]

part2 = [
    [Gen('strontium'), Chip('strontium'), Gen('plutonium'), Chip('plutonium'), Gen('elerium'), Chip('elerium'), Gen('dilithium'), Chip('dilithium')],
    [Gen('thulium'), Gen('ruthenium'), Chip('ruthenium'), Gen('curium'), Chip('curium')],
    [Chip('thulium')],
    [],
]


def solve(state):
    initial_state = State(state)
    nodes = [initial_state]
    shortest = None
    cache = set([initial_state.simplify()])
    # print(cache)
    while nodes:
        current = nodes.pop(0)
        # print('current: {}'.format(current.simplify()))
        for node in current.next_steps():
            simple = node.simplify()
            # print(simple)
            if simple not in cache:
                # print('cached')
                cache.add(simple)
            else:
                # print('pruned')
                continue
            try:
                if node.success:
                    if shortest is None or shortest > node.moves:
                        shortest = node.moves
                        print(shortest)
                else:
                    if shortest is None or node.moves < shortest:
                        # print('append')
                        nodes.append(node)
            except Irradiated:
                # print('irradiated')
                continue

    return shortest


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Test 1: {}".format(solve(test_data)))
    print("Part 1: {}".format(solve(part1)))
    print("Part 2: {}".format(solve(part2)))
