def count_chars(string):
    r"""
    >>> count_chars(r'""')
    (2, 0)
    >>> count_chars(r'"abc"')
    (5, 3)
    >>> count_chars(r'"aaa\"aaa"')
    (10, 7)
    >>> count_chars(r'"\x27"')
    (6, 1)
    """
    code_chars = 2
    mem_chars = 0
    string = string[1:-1]  # strip double quotes

    stringiter = iter(string)
    for char in stringiter:
        code_chars += 1
        mem_chars += 1
        if char == '\\':
            char = stringiter.next()
            code_chars += 1
            if char in ['"', '\\']:
                pass
            elif char == 'x':
                code_chars += 2
                stringiter.next()
                stringiter.next()
            else:
                raise ValueError(char)
    return code_chars, mem_chars


def reencode_string(string):
    r"""
    >>> reencode_string(r'""')
    '"\\"\\""'
    >>> reencode_string(r'"abc"')
    '"\\"abc\\""'
    >>> reencode_string(r'"aaa\"aaa"')
    '"\\"aaa\\\\\\"aaa\\""'
    >>> reencode_string(r'"\x27"')
    '"\\"\\\\x27\\""'
    """
    new_string = '"'
    for char in string:
        if char in ['"', '\\']:
            new_string += "\\"
        new_string += char
    return new_string + '"'


def adventofcode():
    with open('8.txt') as input_file:
        strings = input_file.readlines()

    total = 0
    total2 = 0
    for string in strings:
        code_chars, mem_chars = count_chars(string)
        reencode_chars = len(reencode_string(string))
        total += (code_chars - mem_chars)
        total2 += (reencode_chars - code_chars)
    return total, total2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
