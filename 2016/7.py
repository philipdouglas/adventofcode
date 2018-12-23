import re

supernet_re = re.compile(r'(?:^|\])([a-z]+)(?:\[|$)')
hypernet_re = re.compile(r'\[([a-z]+)\]')


def is_abba(abba):
    """
    >>> is_abba('abba')
    True
    >>> is_abba('qrst')
    False
    >>> is_abba('aba')
    False
    >>> is_abba('aaaa')
    False
    """
    return len(abba) == 4 and abba[0] != abba[1] and abba[:2] == abba[:-3:-1]


def test(strings, function, length=4):
    for string in strings:
        if len(string) < length:
            continue
        for index in range(0, len(string) - length + 1):
            substring = string[index:index + length]
            if function(substring):
                return True
    return False


def supports_tls(addr):
    """
    >>> supports_tls('abba[mnop]qrst')
    True
    >>> supports_tls('abcd[bddb]xyyx')
    False
    >>> supports_tls('aaaa[qwer]tyui')
    False
    >>> supports_tls('ioxxoj[asdfgh]zxcvbn')
    True
    """
    if test(hypernet_re.findall(addr), is_abba):
        return False
    return test(supernet_re.findall(addr), is_abba)


def is_aba(aba):
    """
    >>> is_aba('xyx')
    True
    >>> is_aba('aba')
    True
    >>> is_aba('ababa')
    False
    >>> is_aba('abc')
    False
    """
    return len(aba) == 3 and aba[0] == aba[-1] and aba[0] != aba[1]


def make_bab(aba):
    """
    >>> make_bab('xyx')
    'yxy'
    >>> make_bab('aba')
    'bab'
    """
    return ''.join([aba[1], aba[0], aba[1]])


def supports_ssl(addr):
    """
    >>> supports_ssl('aba[bab]xyz')
    True
    >>> supports_ssl('xyx[xyx]xyx')
    False
    >>> supports_ssl('aaa[kek]eke')
    True
    >>> supports_ssl('zazbz[bzb]cdb')
    True
    """
    abas = set()
    for string in supernet_re.findall(addr):
        if len(string) < 3:
            continue
        for index in range(0, len(string) - 2):
            substring = string[index:index + 3]
            if is_aba(substring):
                abas.add(substring)
    if not abas:
        return False
    babs = {make_bab(aba) for aba in abas}
    for match in hypernet_re.findall(addr):
        for bab in babs:
            if bab in match:
                return True
    return False


def check_ips(lines, check):
    count = 0
    for line in lines:
        count += 1 if check(line.strip()) else 0
    return count


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('7input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        print("Part 1: {}".format(check_ips(lines, supports_tls)))
        print("Part 2: {}".format(check_ips(lines, supports_ssl)))
