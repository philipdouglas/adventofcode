from computer import TogglePuter


class BadSignal(Exception):
    def __init__(self, signal):
        self.message = str(signal)


class InfiniteLoop(Exception):
    pass


class SignalPuter(TogglePuter):
    def __init__(self):
        super().__init__()
        self.signal = []

    def out(self, x):
        value = self._get_value(x)
        self.signal.append(value)
        if value == len(self.signal) % 2:
            raise BadSignal(self.signal)
        if len(self.signal) > 10:
            raise InfiniteLoop
        self.pc += 1


def find_input(instructions):
    aval = 0
    while True:
        try:
            computer = SignalPuter()
            computer.a = aval
            computer.run(instructions, debug=False)
        except BadSignal:
            # print("{}: {}".format(aval, computer.signal))
            aval += 1
        except InfiniteLoop:
            return aval


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('25input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        print("Part 1: {}".format(find_input(lines)))
