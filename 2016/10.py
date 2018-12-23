import re

test_data = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


class Bot:
    def __init__(self, number):
        self.number = number
        self.low_value = None
        self.high_value = None

        self.give_low = None
        self.give_high = None

        self._values = []

    @classmethod
    def set_compare(cls, value1, value2):
        cls._comp1 = value1
        cls._comp2 = value2

    def add_value(self, value):
        self._values.append(value)
        if len(self._values) > 2:
            raise Exception("{}: Too many values: {}".format(
                self.number, self._values))
        if len(self._values) == 2:
            if self._comp1 in self._values and self._comp2 in self._values:
                Bot.part1 = self
            self._values.sort()
            self.low_value = self._values[0]
            self.high_value = self._values[1]
        self.run()

    def add_instruction(self, low, high):
        self.give_low = low
        self.give_high = high
        self.run()

    def run(self):
        if None in [self.low_value, self.high_value, self.give_high, self.give_low]:
            return
        self.give_low.add_value(self.low_value)
        self.low_value = None
        self.give_high.add_value(self.high_value)


class Output(Bot):
    def add_value(self, value):
        self.value = value


value_re = re.compile(
    r'value (\d+) goes to bot (\d+)')
give_re = re.compile(
    r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')


def process(instructions, compare1, compare2):
    """
    >>> process(test_data.split('\\n'), 2, 5)
    Part 1: 2
    Part 2: 30
    """
    Bot.set_compare(compare1, compare2)
    bots = {}
    outputs = {}

    def get_bot(num):
        if num not in bots:
            bots[num] = Bot(num)
        return bots[num]

    def get_out(num):
        if num not in outputs:
            outputs[num] = Output(num)
        return outputs[num]

    for instruction in instructions:
        match = value_re.match(instruction)
        if match:
            value = int(match.group(1))
            bot_num = int(match.group(2))
            get_bot(bot_num).add_value(value)
            continue
        match = give_re.match(instruction)
        if match:
            bot = int(match.group(1))
            low = int(match.group(3))
            high = int(match.group(5))

            get_low = get_bot if match.group(2) == 'bot' else get_out
            get_high = get_bot if match.group(4) == 'bot' else get_out

            get_bot(bot).add_instruction(get_low(low), get_high(high))
        else:
            raise Exception(instruction)

    print("Part 1: {}".format(Bot.part1.number))
    part2 = get_out(0).value * get_out(1).value * get_out(2).value
    print("Part 2: {}".format(part2))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('10input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        process(lines, 17, 61)
