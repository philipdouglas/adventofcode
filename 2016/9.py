import re

marker_re = re.compile(r'\((\d+)x(\d+)\)')


def decompress(text, ver2=False):
    """
    >>> decompress('ADVENT')
    'ADVENT'
    >>> decompress('A(1x5)BC')
    'ABBBBBC'
    >>> decompress('(3x3)XYZ')
    'XYZXYZXYZ'
    >>> decompress('A(2x2)BCD(2x2)EFG')
    'ABCBCDEFEFG'
    >>> decompress('(6x1)(1x3)A')
    '(1x3)A'
    >>> decompress('X(8x2)(3x3)ABCY')
    'X(3x3)ABC(3x3)ABCY'
    >>> decompress('(10x10)ABCDEFGHIJK')
    'ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJK'
    >>> decompress('(3x3)XYZ', True)
    'XYZXYZXYZ'
    >>> decompress('X(8x2)(3x3)ABCY', True)
    'XABCABCABCABCABCABCY'
    >>> len(decompress('(27x12)(20x12)(13x14)(7x10)(1x12)A', True))
    241920
    >>> print(len(decompress('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', True)))
    445
    """
    decompressed = []
    text = list(text)
    while text:
        if text[0] == '(':
            text.pop(0)
            repeat_len = ''
            repeat_times = ''
            while text[0] != 'x':
                repeat_len += text.pop(0)
            text.pop(0)
            while text[0] != ')':
                repeat_times += text.pop(0)
            text.pop(0)
            repeat_len = int(repeat_len)
            repeat_times = int(repeat_times)

            if not ver2:
                decompressed += text[:repeat_len] * repeat_times
                text = text[repeat_len:]
            else:
                text = (text[:repeat_len] * repeat_times) + text[repeat_len:]
        else:
            char = text.pop(0)
            if char != '\n':
                decompressed.append(char)
    return ''.join(decompressed)


def decompress_count(text):
    """
    >>> decompress_count('(3x3)XYZ')
    9
    >>> decompress_count('X(8x2)(3x3)ABCY')
    20
    >>> decompress_count('(27x12)(20x12)(13x14)(7x10)(1x12)A')
    241920
    >>> decompress_count('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
    445
    """
    length = 0
    text = list(text)
    while text:
        if text[0] == '(':
            text.pop(0)
            repeat_len = ''
            repeat_times = ''
            while text[0] != 'x':
                repeat_len += text.pop(0)
            text.pop(0)
            while text[0] != ')':
                repeat_times += text.pop(0)
            text.pop(0)
            repeat_len = int(repeat_len)
            repeat_times = int(repeat_times)

            length += decompress_count(text[:repeat_len]) * repeat_times
            text = text[repeat_len:]
        else:
            char = text.pop(0)
            if char != '\n':
                length += 1
    return length



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('9input.txt', 'r') as inputfile:
        text = inputfile.read()
        part1 = decompress(text)
        print("Part 1: {}".format(len(part1)))
        print("Part 2: {}".format(decompress_count(text)))
