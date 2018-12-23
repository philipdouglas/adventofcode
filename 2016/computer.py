class Computer:
    def __init__(self):
        self.pc = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.program = []

    def __str__(self):
        program = [(prog[0].__name__, prog[1]) for prog in self.program]
        return "a: {} b: {} c: {} d:{} pc:{}\n{}".format(
            self.a, self.b, self.c, self.d, self.pc, program)

    def _get_value(self, arg):
        try:
            value = getattr(self, arg)
        except (AttributeError, TypeError):
            value = int(arg)
        return value

    def cpy(self, x, y):
        """
        >>> c = Computer()
        >>> c.a = 4
        >>> c.cpy('a', 'b')
        >>> c.b
        4
        >>> c.pc
        1
        >>> c.cpy(7, 'b')
        >>> c.b
        7
        >>> c.cpy('8', 'b')
        >>> c.b
        8
        """
        setattr(self, y, self._get_value(x))
        self.pc += 1

    def inc(self, x):
        """
        >>> c = Computer()
        >>> c.a = 4
        >>> c.inc('a')
        >>> c.a
        5
        >>> c.pc
        1
        """
        setattr(self, x, getattr(self, x) + 1)
        self.pc += 1

    def dec(self, x):
        """
        >>> c = Computer()
        >>> c.a = 4
        >>> c.dec('a')
        >>> c.a
        3
        >>> c.pc
        1
        """
        setattr(self, x, getattr(self, x) - 1)
        self.pc += 1

    def jnz(self, x, y):
        """
        >>> c = Computer()
        >>> c.jnz(1, 4)
        >>> c.pc
        4
        >>> c.jnz(0, 2)
        >>> c.pc
        5
        >>> c.jnz('a', 2)
        >>> c.pc
        6
        >>> c.inc('a')
        >>> c.pc
        7
        >>> c.jnz('a', 2)
        >>> c.pc
        9
        """
        x_val = self._get_value(x)
        if x_val != 0:
            y_val = self._get_value(y)
            if y_val == -2:
                repeats = abs(x_val)
                other_var, other_step = None, None
                for cmd, args in self.program[self.pc - 2: self.pc]:
                    if args[0] != x:
                        other_var = args[0]
                        other_step = 1 if cmd == self.inc else -1
                setattr(self, x, 0)
                setattr(self, other_var, getattr(
                    self, other_var) + (other_step * repeats))
                self.jnz(x, y)
            else:
                self.pc += y_val
        else:
            self.pc += 1

    def run(self, instructions, debug=False):
        """
        >>> c = Computer()
        >>> c.run(['cpy 41 a', 'inc a', 'inc a', 'dec a', 'jnz a 2', 'dec a'])
        >>> c.a
        42
        """
        cycles = 0
        self.program = []
        for instruction in instructions:
            isnt_bits = instruction.strip().split(' ')
            self.program.append([
                getattr(self, isnt_bits[0]),
                tuple(isnt_bits[1:])
            ])

        if debug:
            print(self)
        while self.pc < len(instructions):
            cycles += 1
            method, args = self.program[self.pc]
            if debug:
                print("{}({})".format(method.__name__, args))
            method(*args)
            if debug:
                print(self)
                input()


class TogglePuter(Computer):
    def tgl(self, x):
        """
        >>> t = TogglePuter()
        >>> t.program = [[t.inc, ('a', )]]
        >>> t.tgl(0)
        >>> t.program[0][0].__name__
        'dec'
        """
        addr = self.pc + self._get_value(x)
        try:
            if len(self.program[addr][1]) == 1:
                if self.program[addr][0] == self.inc:
                    self.program[addr][0] = self.dec
                else:
                    self.program[addr][0] = self.inc
            elif len(self.program[addr][1]) == 2:
                if self.program[addr][0] == self.jnz:
                    self.program[addr][0] = self.cpy
                else:
                    self.program[addr][0] = self.jnz
        except IndexError:
            pass

        self.pc += 1

