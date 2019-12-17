from itertools import chain, cycle

from aocd.models import Puzzle

from computer import Computer
from coord import Coord
from util import inspect


def compute_intersections(rows):
    """
    >>> compute_intersections(["..#..........","..#..........","##O####...###","#.#...#...#.#","##O###O###O##","..#...#...#..","..#####...^.."])
    76
    """
    scaffold = set()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != '.':
                scaffold.add(Coord(x, y))
    intersections = (scaf for scaf in scaffold if set(scaf.neighbours) <= scaffold)
    return sum(scaf.x * scaf.y for scaf in intersections)


def part1(program):
    computer = Computer(program)
    chars = []
    while not computer.halted:
        next_char = computer.run()
        chars.append(chr(next_char))
    rows = ''.join(chars).split('\n')

    return compute_intersections(rows)


START_TURNS = (
    (Coord(0, -1), []),
    (Coord(1, 0), ['R']),
    (Coord(0, 1), ['R', 'R']),
    (Coord(-1, 0), ['L']),
)


def movement_instructions(rows):
    """
    >>> movement_instructions(["..#..........","..#..........","##O####...###","#.#...#...#.#","##O###O###O##","..#...#...#..","..#####...^.."])
    ['4', 'R', '2', 'R', '2', 'R', '12', 'R', '2', 'R', '6', 'R', '4', 'R', '4', 'R', '6']
    >>> movement_instructions(["#######...#####","#.....#...#...#","#.....#...#...#","......#...#...#","......#...###.#","......#.....#.#","^########...#.#","......#.#...#.#","......#########","........#...#..","....#########..","....#...#......","....#...#......","....#...#......","....#####......"])
    ['R', '8', 'R', '8', 'R', '4', 'R', '4', 'R', '8', 'L', '6', 'L', '2', 'R', '4', 'R', '4', 'R', '8', 'R', '8', 'R', '8', 'L', '6', 'L', '2']
    """
    scaffold = set()
    pos = None
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != '.':
                scaffold.add(Coord(x, y))
            if char == '^':
                pos = Coord(x, y)

    instructions = []
    for direction, turn in START_TURNS:
        if (pos + direction) in scaffold:
            instructions += turn
            break
    else:
        raise Exception("Can't find next scaffold!")

    while True:
        dist = 0
        while (pos + direction) in scaffold:
            dist += 1
            pos += direction
        instructions.append(str(dist))

        if (pos + direction.rotate_left()) in scaffold:
            instructions.append('R')
            direction = direction.rotate_left()
        elif (pos + direction.rotate_right()) in scaffold:
            instructions.append('L')
            direction = direction.rotate_right()
        else:
            break

    return instructions


def compiler(instructions):
    """
    >>> compiler(['R', '8', 'R', '8', 'R', '4', 'R', '4', 'R', '8', 'L', '6', 'L', '2', 'R', '4', 'R', '4', 'R', '8', 'R', '8', 'R', '8', 'L', '6', 'L', '2'])
    [['A','B','C','B','A','C'], ['R','8','R','8'], ['R','4','R','4','R','8'], ['L','6','L','2']]
    """


def move_to_ascii(move):
    return [ord(char) for char in move]


def run_program(program, moves, debug=False):
    moves = [list(chain.from_iterable(zip(line, cycle(',')))) for line in moves]
    moves = [line[:-1] + ['\n'] for line in moves]
    moves = list(chain.from_iterable(moves))
    moves += ['y' if debug else 'n', '\n']
    moves = list(chain.from_iterable(move_to_ascii(move) for move in moves))
    computer = Computer(program, input=moves, mem_override={0: 2})

    if debug:
        row = []
        while not computer.halted:
            row.append(computer.run())
            if row[-1] == ord('\n'):
                print(''.join(chr(cell) for cell in row), end='')
                row = []
        return computer.output

    while not computer.halted:
        computer.run()
    return computer.output


def part2(program):
    computer = Computer(program)
    chars = []
    while not computer.halted:
        next_char = computer.run()
        chars.append(chr(next_char))
    rows = ''.join(chars).split('\n')

    full_moves = movement_instructions(rows)
    # A proper solution for compiler should go here

    moves = [
        ['A', 'B', 'B', 'A', 'C', 'A', 'C', 'A', 'C', 'B'],
        ['L', '6', 'R', '12', 'R', '8'],
        ['R', '8', 'R', '12', 'L', '12'],
        ['R', '12', 'L', '12', 'L', '4', 'L', '4'],
    ]

    return run_program(program, moves, False)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=17)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
