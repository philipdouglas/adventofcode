import hashlib
import re

SALT = 'ihaygndm'
triplet_re = re.compile(r'(.)\1\1')


class HashCache:
    def __init__(self, stretch=False):
        self._cache = {}
        self.stretch = stretch

    @staticmethod
    def md5(string):
        md5 = hashlib.md5()
        md5.update(string.encode())
        return md5.hexdigest()

    def __getitem__(self, key):
        if key not in self._cache:
            md5hash = self.md5(key)
            if self.stretch:
                for _ in range(2016):
                    md5hash = self.md5(md5hash)
            self._cache[key] = md5hash
        return self._cache[key]


def generate_keys(salt, stretch=False):
    """
    >>> generate_keys('abc')
    22728
    >>> generate_keys('abc', True)
    22551
    """
    index = -1
    keys = []
    hash_cache = HashCache(stretch=stretch)
    while len(keys) < 64:
        index += 1
        to_hash = salt + str(index)
        match = triplet_re.search(hash_cache[to_hash])
        if match:
            quint = match.group(1) * 5
            for offset in range(1, 1000):
                to_hash = salt + str(index + offset)
                if quint in hash_cache[to_hash]:
                    keys.append(hash_cache[to_hash])
    return index


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(generate_keys(SALT)))
    print("Part 2: {}".format(generate_keys(SALT, True)))
