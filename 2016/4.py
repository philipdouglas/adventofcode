import re
from string import ascii_lowercase

NAME_RE = re.compile(r'([a-z-]+)-(\d{3})\[([a-z]{5})\]')


def is_real(name):
    """
    >>> is_real('aaa-bbb-z-y-x-123[abxyz]')
    123
    >>> is_real('a-b-c-d-e-f-g-h-987[abcde]')
    987
    >>> is_real('not-a-real-room-404[oarel]')
    404
    >>> is_real('totally-real-room-200[decoy]')
    0
    """
    match = NAME_RE.match(name)
    if not match:
        return False
    counts = {}
    for letter in match.group(1):
        if letter == '-':
            continue
        counts.setdefault(letter, 0)
        counts[letter] += 1
    checksum = sorted(counts.keys())
    checksum = sorted(
        checksum, key=lambda letter: counts[letter], reverse=True)[:5]
    if ''.join(checksum) == match.group(3):
        return int(match.group(2))
    else:
        return 0


def process_rooms(rooms):
    total = 0
    for name in rooms:
        total += is_real(name)
    return total


def decrypt_name(name, sector_id):
    """
    >>> decrypt_name('qzmt-zixmtkozy-ivhz', 343)
    'very encrypted name'
    """
    rotnum = sector_id % 26
    rot = str.maketrans(
        '-' + ascii_lowercase,
        (' ' + ascii_lowercase[rotnum:len(ascii_lowercase)] +
         ascii_lowercase[0:rotnum]),
    )
    return str.translate(name, rot)


def find_north_pole_room(rooms):
    for room in rooms:
        match = NAME_RE.match(room)
        if not match:
            continue
        sector_id = int(match.group(2))
        name = decrypt_name(match.group(1), sector_id)
        if name == 'northpole object storage':
            return sector_id


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('4input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        print("Part 1: {}".format(process_rooms(lines)))
        print("Part 2: {}".format(find_north_pole_room(lines)))
