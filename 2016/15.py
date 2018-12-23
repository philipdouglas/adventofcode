import copy

class Lost(Exception):
    pass

class Disc:
    def __init__(self, positions, start):
        self._positions = positions
        self.position = start
        self.capsule = False

    def tick(self):
        """
        >>> d = Disc(4, 2)
        >>> d.position
        2
        >>> d.tick()
        False
        >>> d.position
        3
        >>> d.tick()
        False
        >>> d.position
        0
        >>> d.capsule = True
        >>> d.tick()
        True
        >>> d.position
        1
        """
        drop_capsule = self.capsule
        self.capsule = False
        self.position += 1
        if self.position == self._positions:
            self.position = 0
        return drop_capsule

    def __str__(self):
        return "{}: {}".format(self.position, self.capsule)


class Machine:
    def __init__(self, discs=[]):
        self.time = 0
        self.discs = discs

    def add_disc(self, disc):
        self.discs.append(disc)

    def tick(self, button=False):
        """
        >>> machine = copy.deepcopy(TEST_INPUT)
        >>> machine.tick(True)
        False
        >>> machine.time
        1
        >>> machine.discs[0].capsule
        True
        >>> machine.tick()
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        Lost
        >>> machine.time
        2
        >>> machine = copy.deepcopy(TEST_INPUT)
        >>> machine.tick() == machine.tick() == machine.tick() == machine.tick() == machine.tick()
        True
        >>> machine.tick(True)
        False
        >>> machine.tick()
        False
        >>> machine.tick()
        True
        """
        in_capsule = button
        try:
            for disc in self.discs:
                out_capsule = disc.tick()
                if in_capsule and disc.position != 0:
                    raise Lost()
                disc.capsule = in_capsule
                in_capsule = out_capsule
            return out_capsule
        finally:
            self.time += 1


TEST_INPUT = Machine([Disc(5, 4), Disc(2, 1)])
PART1_INPUT = Machine([
    Disc(13, 10),
    Disc(17, 15),
    Disc(19, 17),
    Disc(7, 1),
    Disc(5, 0),
    Disc(3, 1),
])
PART2_INPUT = copy.deepcopy(PART1_INPUT)
PART2_INPUT.add_disc(Disc(11, 0))


def get_capsule(start_machine):
    wait = -1
    last_wait = start_machine
    while True:
        wait += 1
        if wait % 10000 == 0:
            print(wait)
        machine = copy.deepcopy(last_wait)
        try:
            if machine.tick(button=True):
                return wait
            while machine.tick() is False:
                continue
            return wait
        except Lost:
            # print("lost")
            continue
        finally:
            last_wait.tick()


TDISCS = (5, 2)
TOFFSETS = (4, 1)

P1DISCS = (13, 17, 19, 7, 5, 3)
P1OFFSETS = (10, 15, 17, 1, 0, 1)

P2DISCS = (13, 17, 19, 7, 5, 3, 11)
P2OFFSETS = (10, 15, 17, 1, 0, 1, 0)


def check_time(time, discs, offsets):
    """
    >>> check_time(0, TDISCS, TOFFSETS)
    False
    >>> check_time(5, TDISCS, TOFFSETS)
    True
    """
    for tplus in range(len(discs)):
        position = (1 + time + tplus + offsets[tplus]) % discs[tplus]
        # print("({} + {}) % {} = {}".format(time + 1 + tplus, offsets[tplus], discs[tplus], position))
        if position != 0:
            return False
    return True


def get_capsule_smart(discs, offsets):
    time = 0
    while True:
        if check_time(time, discs, offsets):
            return time
        time += 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # print("Test 1: {}".format(get_capsule(TEST_INPUT)))
    # print("Part 1: {}".format(get_capsule(PART1_INPUT)))
    # print("Part 1: {}".format(get_capsule(PART2_INPUT)))
    print("Test 1: {}".format(get_capsule_smart(TDISCS, TOFFSETS)))
    print("Part 1: {}".format(get_capsule_smart(P1DISCS, P1OFFSETS)))
    print("Part 1: {}".format(get_capsule_smart(P2DISCS, P2OFFSETS)))
