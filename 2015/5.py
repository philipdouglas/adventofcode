VOWELS = ['a', 'e', 'i', 'o', 'u']
NAUGHTY_PAIRS = ['ab', 'cd', 'pq', 'xy']

def is_nice(string):
    """
    >>> is_nice('ugknbfddgicrmopn')
    True
    >>> is_nice('aaa')
    True
    >>> is_nice('jchzalrnumimnmhp')
    False
    >>> is_nice('haegwjzuvuyypxyu')
    False
    >>> is_nice('dvszwmarrgswjxmb')
    False
    """
    vowels = 0
    twice = False
    for index in range(len(string)):
        if vowels < 3 and string[index] in VOWELS:
            vowels += 1
        try:
            if not twice and string[index] == string[index + 1]:
                twice = True
            if string[index:index + 2] in NAUGHTY_PAIRS:
                break
        except IndexError:
            continue
    else:
        return vowels == 3 and twice
    return False

def is_nice2(string):
    """
    >>> is_nice2('qjhvhtzxzqqjkmpb')
    True
    >>> is_nice2('xxyxx')
    True
    >>> is_nice2('uurcxstgmygtbstg')
    False
    >>> is_nice2('ieodomkazucvgmuy')
    False
    """
    repeat_found = False
    pair_found = False
    pairs = {}
    for index in range(len(string)):
        try:
            pair = string[index:index + 2]
            if not pair_found and pairs.setdefault(pair, index + 1) < index:
                pair_found = True
            if not repeat_found and string[index] == string[index + 2]:
                repeat_found = True
        except IndexError:
            pass
        if pair_found and repeat_found:
            return True
    return False



def adventofcode():
    with open('5.txt') as input_file:
        strings = input_file.readlines()
    count = 0
    count2 = 0
    for string in strings:
        if is_nice(string):
            count += 1
        if is_nice2(string):
            count2 += 1
    return count, count2


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    print(adventofcode())
