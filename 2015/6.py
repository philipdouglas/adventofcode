import re

INSTR_REGEX = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')

class Grid:
    def __init__(self, size):
        self.grid = []
        for row_index in range(size):
            self.grid.append([0] * size)

    def parse_instruction(self, instruction):
        match = INSTR_REGEX.match(instruction)
        mode = match.group(1)
        start = (int(match.group(2)), int(match.group(3)))
        end = (int(match.group(4)), int(match.group(5)))
        return mode, start, end

    def apply_instruction(self, instruction):
        """
        >>> grid = Grid(1000)
        >>> grid.count_lights()
        0
        >>> grid.apply_instruction('turn on 0,0 through 999,999')
        >>> grid.count_lights()
        1000000
        >>> grid.apply_instruction('turn off 499,499 through 500,500')
        >>> grid.count_lights()
        999996
        >>> grid = Grid(1000)
        >>> grid.apply_instruction('toggle 0,0 through 999,0')
        >>> grid.count_lights()
        1000
        >>> grid.apply_instruction('toggle 0,0 through 999,0')
        >>> grid.count_lights()
        0
        """
        mode, start, end = self.parse_instruction(instruction)

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                if mode == 'turn on':
                    self.grid[row][column] = 1
                elif mode == 'turn off':
                    self.grid[row][column] = 0
                elif mode == 'toggle':
                    self.grid[row][column] = 0 if self.grid[row][column] else 1

    def apply_instruction2(self, instruction):
        """
        >>> grid = Grid(1000)
        >>> grid.count_lights()
        0
        >>> grid.apply_instruction2('turn off 0,0 through 0,0')
        >>> grid.count_lights()
        0
        >>> grid.apply_instruction2('turn on 0,0 through 0,0')
        >>> grid.count_lights()
        1
        >>> grid.apply_instruction2('toggle 0,0 through 999,999')
        >>> grid.count_lights()
        2000001
        """
        mode, start, end = self.parse_instruction(instruction)

        for row in range(start[0], end[0] + 1):
            for column in range(start[1], end[1] + 1):
                if mode == 'turn on':
                    self.grid[row][column] += 1
                elif mode == 'turn off':
                    self.grid[row][column] = max(self.grid[row][column] - 1, 0)
                elif mode == 'toggle':
                    self.grid[row][column] += 2

    def count_lights(self):
        """
        >>> grid = Grid(2)
        >>> grid.count_lights()
        0
        >>> grid.grid[0][0] = True
        >>> grid.count_lights()
        1
        >>> grid.grid[1][0] = True
        >>> grid.count_lights()
        2
        """
        total = 0
        for row in self.grid:
            total += sum(row)
        return total


def adventofcode():
    with open('6.txt') as input_file:
        instructions = input_file.readlines()

    light_grid = Grid(1000)
    light_grid2 = Grid(1000)
    for instruction in instructions:
        light_grid.apply_instruction(instruction)
        light_grid2.apply_instruction2(instruction)
    return light_grid.count_lights(), light_grid2.count_lights()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
