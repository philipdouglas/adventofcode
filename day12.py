import dataclasses
import itertools
import re
from functools import total_ordering

from aocd.models import Puzzle

from coord import Coord3
from util import inspect

MOON_RE = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')


@dataclasses.dataclass
class Moon:
    pos: Coord3
    vel: Coord3

    @property
    def potential_energy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    @property
    def kinetic_energy(self):
        return abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)

    @property
    def total_energy(self):
        return self.kinetic_energy * self.potential_energy


def parse(moon):
    match = MOON_RE.match(moon)
    return Moon(
        pos=Coord3(int(match[1]), int(match[2]), int(match[3])),
        vel=Coord3(0, 0, 0)
    )


def part1(moons, target_steps):
    """
    >>> moons = ['<x=-1, y=0, z=2>', '<x=2, y=-10, z=-7>', '<x=4, y=-8, z=8>', '<x=3, y=5, z=-1>']
    >>> part1(moons, 10)
    179
    >>> moons = ['<x=-8, y=-10, z=0>', '<x=5, y=5, z=10>', '<x=2, y=-7, z=3>', '<x=9, y=-8, z=-3>']
    >>> part1(moons, 100)
    1940
    """
    moons = [parse(moon) for moon in moons]
    for step in range(target_steps):
        for moon_a, moon_b in itertools.permutations(moons, 2):
            dx, dy, dz = 0, 0, 0
            if moon_a.pos.x < moon_b.pos.x:
                dx = 1
            elif moon_a.pos.x > moon_b.pos.x:
                dx = -1
            if moon_a.pos.y < moon_b.pos.y:
                dy = 1
            elif moon_a.pos.y > moon_b.pos.y:
                dy = -1
            if moon_a.pos.z < moon_b.pos.z:
                dz = 1
            elif moon_a.pos.z > moon_b.pos.z:
                dz = -1
            moon_a.vel = moon_a.vel + Coord3(dx, dy, dz)
        for moon in moons:
            moon.pos = moon.pos + moon.vel
    return sum(moon.total_energy for moon in moons)



# def part2(moons):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=12)
    moons = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(moons, 1000), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(moons), prefix='Part 2: ')
