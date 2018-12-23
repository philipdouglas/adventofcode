import re

INSTRUCTION_RE = re.compile(r'(hlf|tpl|inc|jmp|jie|jio) (a|b)?,? ?([-+]\d+)?')


class Computer:
    def __init__(self, instructions):
        self.registers = {
            'a': 0,
            'b': 0,
        }
        self.pc = 0
        self.instructions = [
            self.parse_line(instruction) for instruction in instructions]

    def hlf(self, address):
        """
        >>> c = Computer([])
        >>> c.registers['a'] = 4
        >>> c.hlf('a')
        >>> c.registers['a']
        2
        >>> c.pc
        1
        """
        self.registers[address] //= 2
        self.pc += 1

    def tpl(self, address):
        """
        >>> c = Computer([])
        >>> c.registers['a'] = 6
        >>> c.tpl('a')
        >>> c.registers['a']
        18
        >>> c.pc
        1
        """
        self.registers[address] *= 3
        self.pc += 1

    def inc(self, address):
        """
        >>> c = Computer([])
        >>> c.registers['a'] = 6
        >>> c.inc('a')
        >>> c.registers['a']
        7
        >>> c.pc
        1
        """
        self.registers[address] += 1
        self.pc += 1

    def jmp(self, offset):
        """
        >>> c = Computer([])
        >>> c.jmp(5)
        >>> c.pc
        5
        """
        self.pc += offset

    def jie(self, address, offset):
        """
        >>> c = Computer([])
        >>> c.registers['a'] = 3
        >>> c.jie('a', 5)
        >>> c.pc
        1
        >>> c.registers['a'] = 4
        >>> c.jie('a', 5)
        >>> c.pc
        6
        """
        if self.registers[address] % 2 == 0:
            self.pc += offset
        else:
            self.pc += 1

    def jio(self, address, offset):
        """
        >>> c = Computer([])
        >>> c.registers['a'] = 1
        >>> c.jio('a', 5)
        >>> c.pc
        5
        >>> c.registers['a'] = 4
        >>> c.jio('a', 5)
        >>> c.pc
        6
        """
        if self.registers[address] == 1:
            self.pc += offset
        else:
            self.pc += 1


    @staticmethod
    def parse_literal(token):
        """
        >>> Computer.parse_literal('-1')
        -1
        >>> Computer.parse_literal('+145')
        145
        """
        return int(token[1:]) * (-1 if token[0] == '-' else 1)

    @staticmethod
    def parse_line(line):
        match = INSTRUCTION_RE.match(line)
        if match.group(1) in ['hlf', 'tpl', 'inc']:
            args = (match.group(2), )
        elif match.group(1) in ['jmp']:
            args = (Computer.parse_literal(match.group(3)), )
        elif match.group(1) in ['jio', 'jie']:
            args = (match.group(2), Computer.parse_literal(match.group(3)))
        else:
            raise Exception("WHAAAAT " + line)
        return match.group(1), args

    def execute(self, verbose=False):
        """
        >>> c = Computer(['inc a', 'jio a, +2', 'tpl a', 'inc a'])
        >>> c.execute()
        >>> c.registers['a']
        2
        """
        while self.pc < len(self.instructions):
            instruction, args = self.instructions[self.pc]
            if verbose:
                print('pc: {}, regs: {}'.format(self.pc, self.registers))
                print('{} {}'.format(instruction, args))
            getattr(self, instruction)(*args)


def adventofcode():
    with open('23.txt') as input_file:
        instructions = input_file.readlines()

    computer = Computer(instructions)
    computer.execute()
    part1 = computer.registers['b']

    computer = Computer(instructions)
    computer.registers['a'] = 1
    computer.execute()
    part2 = computer.registers['b']

    return part1, part2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
