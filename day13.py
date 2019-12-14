from aocd.models import Puzzle

from computer import Computer, Halted
from coord import Coord
from util import inspect


def part1(program):
    screen = {}
    computer = Computer(program)
    while not computer.halted:
        try:
            x = computer.run()
            y = computer.run()
            pos = Coord(x, y)
            tile_id = computer.run()
            screen[pos] = tile_id
        except Halted:
            pass
    return len([tile for tile in screen.values() if tile == 2])


TILES = {
    0: ' ',
    1: '█',
    2: '#',
    3: '━',
    4: 'o',
}


def print_screen(screen, score):
    print(f"Score: {score}")

    minx_coord = min(c.x for c in screen.keys())
    miny_coord = min(c.y for c in screen.keys())
    maxx_coord = max(c.x for c in screen.keys())
    maxy_coord = max(c.y for c in screen.keys())

    rows = []
    for y in range(miny_coord, maxy_coord + 1):
        row = []
        for x in range(minx_coord, maxx_coord + 1):
            tile = screen[Coord(x, y)]
            row.append(TILES[tile])
        rows.append(''.join(row))
    print('\n'.join(rows))


def part2(program):
    screen = {}
    score = None
    last_ball_x = 0
    last_paddle_x = 0

    def paddle_ai():
        return (last_ball_x > last_paddle_x) - (last_ball_x < last_paddle_x)

    computer = Computer(program, mem_override={0: 2}, input=paddle_ai)

    computer.input_func = paddle_ai
    while not computer.halted:
        try:
            x = computer.run()
            y = computer.run()
            pos = Coord(x, y)
            if pos == Coord(-1, 0):
                score = computer.run()
            else:
                screen[pos] = computer.run()
                if screen[pos] == 3:
                    last_paddle_x = pos.x
                if screen[pos] == 4:
                    last_ball_x = pos.x
        except Halted:
            pass
    return score


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=13)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
