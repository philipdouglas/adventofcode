from hashlib import md5


def adventofcode(inp, zeroes):
    """
    >>> adventofcode('abcdef', 5)
    609043
    >>> adventofcode('pqrstuv', 5)
    1048970
    """
    answer = 0
    while not md5(inp + str(answer)).hexdigest().startswith('0' * zeroes):
        answer += 1
    return answer

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode('iwrupvqb', 5))
    print(adventofcode('iwrupvqb', 6))

# cbob: bgvyzdsv
