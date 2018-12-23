import hashlib

DOOR_ID = 'ffykfhsq'

def generate_password(door_id, advanced=False):
    """
    >>> generate_password('abc')
    '18f47a30'
    >>> generate_password('abc', True)
    '05ace8e3'
    """
    index = 0
    password = [None] * 8 if advanced else []
    while len(password) < 8 or None in password:
        md5 = hashlib.md5()
        md5.update((door_id + str(index)).encode())
        md5 = md5.hexdigest()
        if md5[:5] == '00000':
            if not advanced:
                password.append(md5[5])
            else:
                try:
                    position = int(md5[5])
                    if password[position] is None:
                        password[position] = md5[6]
                except (IndexError, ValueError):
                    pass
        index += 1
    return ''.join(password)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(generate_password(DOOR_ID)))
    print("Part 2: {}".format(generate_password(DOOR_ID, True)))
