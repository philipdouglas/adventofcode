import itertools


def scramble(string, instructions):
    """
    >>> scramble('abc', ['swap position 1 with position 2'])
    'acb'
    >>> scramble('abc', ['swap letter c with letter a'])
    'cba'
    >>> scramble('abcde', ['rotate right 1 step'])
    'eabcd'
    >>> scramble('abcde', ['rotate left 1 step'])
    'bcdea'
    >>> scramble('abdec', ['rotate based on position of letter b'])
    'ecabd'
    >>> scramble('abdec', ['rotate based on position of letter c'])
    'cabde'
    >>> scramble('edcba', ['reverse positions 0 through 4'])
    'abcde'
    >>> scramble('bcdea', ['move position 1 to position 4'])
    'bdeac'
    """
    string = list(string)
    for instruction in instructions:
        pieces = instruction.split()
        if pieces[0] == 'swap':
            X = pieces[2]
            Y = pieces[5]
            if pieces[1] == 'position':
                X = int(X)
                Y = int(Y)
            else:
                X = string.index(X)
                Y = string.index(Y)
            string[X], string[Y] = string[Y], string[X]
        elif pieces[0] == 'rotate':
            direction = 1 if pieces[1] == 'left' else -1
            try:
                steps = int(pieces[2])
            except ValueError:
                index = string.index(pieces[6])
                steps = 1 + index + (1 if index >= 4 else 0)
            steps %= len(string)
            steps *= direction
            string = string[steps:] + string[:steps]
        elif pieces[0] == 'reverse':
            X = int(pieces[2])
            Y = int(pieces[4]) + 1
            string[X:Y] = string[X:Y][::-1]
        elif pieces[0] == 'move':
            X = int(pieces[2])
            Y = int(pieces[5])
            string.insert(Y, string.pop(X))

    return ''.join(string)


# def unscramble(goal, instructions):
#     for password in itertools.permutations(goal, len(goal)):
#         if scramble(password, instructions) == goal:
#             return ''.join(password)

REVERSE_ROTATE = {0: -7, 1: 1, 2: -2, 3: 2, 4: -1, 5: 3, 6: 0, 7: 4}


def unscramble(string, instructions):
    """
    >>> unscramble('acb', ['swap position 1 with position 2'])
    'abc'
    >>> unscramble('cba', ['swap letter c with letter a'])
    'abc'
    >>> unscramble('eabcd', ['rotate right 1 step'])
    'abcde'
    >>> unscramble('bcdea', ['rotate left 1 step'])
    'abcde'
    >>> unscramble('habcdefg', ['rotate based on position of letter a'])
    'abcdefgh'
    >>> unscramble('efghabcd', ['rotate based on position of letter a'])
    'defghabc'
    >>> unscramble('abcde', ['reverse positions 0 through 4'])
    'edcba'
    >>> unscramble('bdeac', ['move position 1 to position 4'])
    'bcdea'
    """
    string = list(string)
    for instruction in reversed(instructions):
        pieces = instruction.split()
        if pieces[0] == 'swap':
            X = pieces[2]
            Y = pieces[5]
            if pieces[1] == 'position':
                X = int(X)
                Y = int(Y)
            else:
                X = string.index(X)
                Y = string.index(Y)
            string[X], string[Y] = string[Y], string[X]
        elif pieces[0] == 'rotate':
            direction = -1 if pieces[1] == 'left' else 1
            try:
                steps = int(pieces[2])
            except ValueError:
                index = string.index(pieces[6])
                steps = REVERSE_ROTATE[index]
            steps %= len(string)
            steps *= direction
            string = string[steps:] + string[:steps]
        elif pieces[0] == 'reverse':
            X = int(pieces[2])
            Y = int(pieces[4]) + 1
            string[X:Y] = string[X:Y][::-1]
        elif pieces[0] == 'move':
            Y = int(pieces[2])
            X = int(pieces[5])
            removed = string.pop(X)
            string.insert(Y, removed)

    return ''.join(string)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('21test.txt') as inputfile:
        print(f"Test 1: {scramble('abcde', inputfile.readlines())}")

    with open('21input.txt') as inputfile:
        instructions = inputfile.readlines()
        print(f"Part 1: {scramble('abcdefgh', instructions)}")
        print(f"Part 2: {unscramble('fbgdceah', instructions)}")
