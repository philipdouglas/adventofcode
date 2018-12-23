import re
from string import ascii_lowercase as alphabet

def is_valid(password):
    """
    >>> is_valid('abcdffaa')
    True
    >>> is_valid('ghjaabcc')
    True
    >>> is_valid('hijklmmn')
    False
    >>> is_valid('abbceffg')
    False
    >>> is_valid('abbcegjk')
    False
    """
    if re.search(r'[iol]', password):
        return False
    pairs = 0
    index = 0
    while index < len(password) and pairs < 2:
        try:
            if password[index] == password[index + 1]:
                pairs += 1
                index += 1
        except IndexError:
            pass
        index += 1
    if pairs < 2:
        return False
    index = 0
    while index < len(password) - 2:
        try:
            cur = password[index]
            cur_loc = alphabet.find(cur)
            if password[index:index + 3] == alphabet[cur_loc:cur_loc + 3]:
                break
            index += 1
        except IndexError:
            pass
    else:
        return False
    return True


def increment(password):
    """
    >>> increment('xx')
    'xy'
    >>> increment('xy')
    'xz'
    >>> increment('xz')
    'ya'
    """
    index = -1
    new_password = []
    while -index <= len(password):
        try:
            new_password.append(alphabet[alphabet.find(password[index]) + 1])
            break
        except IndexError:
            new_password.append('a')
            index -= 1
    return password[:index] + ''.join(reversed(new_password))


def new(password):
    """
    >>> new('abcdefgh')
    'abcdffaa'
    >>> new('ghijklmn')
    'ghjaabcc'
    """
    while True:
        password = increment(password)
        if is_valid(password):
            break
    return password


def adventofcode(old):
    return new(old)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    second = adventofcode('hxbxwxba')
    print(second)
    print(adventofcode(second))
