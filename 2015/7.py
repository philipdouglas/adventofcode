import operator
import re

SIGNAL_RE = re.compile(r'^(\d+|[a-z]+) ?$')
OP_RE = re.compile(r'^(\d+|[a-z]+) (AND|OR|LSHIFT|RSHIFT) (\d+|[a-z]+) ?$')
NOT_RE = re.compile(r'^NOT (\d+|[a-z]+) ?$')


class Circuit:
    def __init__(self, filename):
        self.wires = {}

        with open(filename) as input_file:
            instructions = input_file.readlines()

        for instruction in instructions:
            self.add_instruction(instruction)

    def __getitem__(self, key):
        return self.wires.setdefault(key, Wire())

    def wire_or_value(self, string):
        string = string.strip()
        try:
            return Value(string)
        except ValueError:
            return self[string]

    def add_instruction(self, instruction):
        (inp, out) = instruction.split('->')
        out = out.strip()

        op_match = OP_RE.match(inp)
        not_match = NOT_RE.match(inp)
        if SIGNAL_RE.match(inp):
            self[out].input = self.wire_or_value(inp)
        elif op_match:
            self[out].input = Gate(
                op_match.group(2),
                self.wire_or_value(op_match.group(1)),
                self.wire_or_value(op_match.group(3))
            )
        elif not_match:
            self[out].input = Not(self.wire_or_value(not_match.group(1)))
        else:
            raise ValueError(instruction)

    def __str__(self):
        string = ''
        for identifier, wire in self.wires.items():
            string += '{}: {}\n'.format(identifier, wire.output)
        return string


class CircuitNode:
    @property
    def output(self):
        raise NotImplemented


class Wire(CircuitNode):
    def __init__(self):
        self.input = None
        self._output = None

    @property
    def output(self):
        if self._output is None:
            self._output = self.input.output
        return self._output


class Value(CircuitNode):
    def __init__(self, value):
        self.value = int(value)

    @property
    def output(self):
        return self.value


class Gate(CircuitNode):
    OPERATORS = {
        'AND': operator.and_,
        'OR': operator.or_,
        'LSHIFT': operator.lshift,
        'RSHIFT': operator.rshift,
    }

    def __init__(self, op, left, right):
        self.left = left
        self.right = right
        self.func = self.OPERATORS[op]

    @property
    def output(self):
        return self.func(self.left.output, self.right.output)


class Not(CircuitNode):
    def __init__(self, inp):
        self.input = inp

    @property
    def output(self):
        return self.input.output ^ 0xFFFF


if __name__ == "__main__":
    # print(str(Circuit('7example.txt')))
    circuit = Circuit('7.txt')
    result = circuit['a'].output
    print(result)

    circuit.wires['b'].input = Value(result)
    for wire in circuit.wires.values():
        wire._output = None
    print(circuit['a'].output)
