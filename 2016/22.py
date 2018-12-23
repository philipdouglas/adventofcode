from collections import defaultdict
from copy import deepcopy
from itertools import permutations
import re

from coord import BlockCoord

input_re = re.compile(r'\/dev\/grid\/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T')


class Node(BlockCoord):
    def __init__(self, x, y, size, used, avail):
        super().__init__(x, y)
        self.size = size
        self.used = used
        self.avail = avail
        self.goal = False

    def is_adjacent(self, other):
        return self.distance_blocks(other) == 1

    def empty(self):
        self.used = 0
        self.avail = self.size
        self.goal = False

    def add(self, amount):
        self.used += amount
        self.avail -= amount

    def __str__(self):
        string = f"[{self.used}|{self.avail}]"
        if self.goal:
            string += 'G'
        return string

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.used) ^ hash(self.avail) ^ hash(self.goal)


class State:
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        self.moves = 0

    def next_states(self):
        for indexa, indexb in permutations(range(len(self.nodes)), 2):
            a = self.nodes[indexa]
            b = self.nodes[indexb]
            if a.is_adjacent(b) and b.avail >= a.used:
                new_state = deepcopy(self)
                new_state.nodes[indexb].add(a.used)
                if a.goal:
                    new_state.nodes[indexb].goal = a.goal
                new_state.nodes[indexa].empty()
                new_state.moves += 1
                yield new_state

    def __hash__(self):
        return hash(self.nodes)

    def __str__(self):
        data = [' -- '.join([str(node) for node in self.nodes[x:x + 31]]) for x in range(0, len(self.nodes), 31)]
        return '\n'.join(data)

    def score(self):
        for node in self.nodes:
            if node.goal:
                return node.distance_blocks()
        raise Exception(f"Lost the goal: {self.nodes}")


def parse_nodes(lines):
    nodes = []
    goal = None
    for line in lines:
        match = input_re.match(line)
        if match:
            args = [match.group(1), match.group(2), match.group(3),
                    match.group(4), match.group(5)]
            args = [int(arg) for arg in args]
            node = Node(*args)
            if args[1] == 0:
                goal = node
            nodes.append(node)
    goal.goal = True
    return nodes


def get_viable_pairs(nodes):
    viable = []
    for a, b in permutations(nodes, 2):
        if a.used > 0 and a.used < b.avail:
            viable.append((a, b))
    return viable


def solve(nodes):
    start = State(nodes)

    closed_set = set()
    open_set = set([start])
    gscores = {start: 0}
    fscores = defaultdict(lambda: float('inf'))
    fscores[start] = start.score()
    came_from = {}

    while open_set:
        current = sorted(open_set, key=lambda node: fscores[node])[0]
        print(fscores.values())
        if current.nodes[0].goal:
            prev = current
            while prev in came_from:
                print(prev)
                prev = came_from[prev]
            return gscores[current]

        open_set.remove(current)
        closed_set.add(current)

        for state in current.next_states():
            if state in closed_set:
                continue

            gscore = gscores[current] + 1
            if state not in open_set:
                open_set.add(state)
            elif gscore >= gscores[state]:
                continue

            gscores[state] = gscore
            fscores[state] = gscore + state.score()
            came_from[state] = current


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # with open('22test.txt', 'r') as test_file:
    #     nodes = parse_nodes(test_file.readlines())
    #     print(f"Test 2: {solve(nodes)}")

    with open('22input.txt', 'r') as input_file:
        nodes = parse_nodes(input_file.readlines())

        print(f"Part 1: {get_viable_pairs(nodes)}")
        print(State(nodes))
        # print(f"Part 2: {solve(nodes)}")

# NB: I abandoned the programmatic solution here and did it manually from the
# pretty print of the grid
# It turnes out there is only one node with enough free space to hold the goal's
# worth, so you just shuffle that in the y=0 column, move it to the slot below
# the goal, and then move the goal by shifting it, and then shifting the data in
# the next slot around it
