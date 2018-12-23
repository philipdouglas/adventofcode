import hashlib


class Rooms:
    DIRECTIONS = ('U', 'D', 'L', 'R')

    def __init__(self, initial):
        self.initial = initial

    @staticmethod
    def is_room(route):
        """
        >>> Rooms.is_room('DUL')
        False
        >>> Rooms.is_room('DUR')
        True
        >>> Rooms.is_room('DUU')
        False
        >>> Rooms.is_room('DUD')
        True
        """
        ups = route.count('U') - route.count('D')
        lefts = route.count('L') - route.count('R')
        return not(ups > 0 or ups <= -4 or lefts > 0 or lefts <= -4)

    @staticmethod
    def is_vault(route):
        """
        >>> Rooms.is_vault('DUL')
        False
        >>> Rooms.is_vault('DU')
        False
        >>> Rooms.is_vault('RRRDDD')
        True
        """
        downs = route.count('D') - route.count('U')
        rights = route.count('R') - route.count('L')
        return downs == 3 and rights == 3

    @staticmethod
    def is_open(letter):
        """
        >>> Rooms.is_open('b')
        True
        >>> Rooms.is_open('1')
        False
        >>> Rooms.is_open('a')
        False
        """
        return letter in ('b', 'c', 'd', 'e', 'f')

    @staticmethod
    def md5(string):
        md5 = hashlib.md5()
        md5.update(string.encode())
        return md5.hexdigest()

    def get_options(self, route):
        """
        >>> r = Rooms('hijkl')
        >>> list(r.get_options('hijkl'))
        ['hijklD']
        >>> list(r.get_options('hijklD'))
        ['hijklDU', 'hijklDR']
        >>> list(r.get_options('hijklDU'))
        ['hijklDUR']
        >>> list(r.get_options('hijklDUR'))
        []
        """
        hashed = self.md5(route)
        for index in range(4):
            option = route + self.DIRECTIONS[index]
            if self.is_open(hashed[index]) and self.is_room(option):
                yield option

    def find_shortest_route(self):
        """
        >>> Rooms('ihgpwlah').find_shortest_route()
        'DDRRRD'
        >>> Rooms('kglvqrro').find_shortest_route()
        'DDUDRLRRUDRD'
        >>> Rooms('ulqzkmiv').find_shortest_route()
        'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
        """
        routes = [self.initial]
        shortest = None
        while routes:
            route = routes.pop()
            if shortest and len(route) >= len(shortest):
                continue
            if self.is_vault(route):
                shortest = route
                continue

            for option in self.get_options(route):
                routes.append(option)

        return shortest.lstrip(self.initial)


    def find_longest_route(self):
        """
        >>> Rooms('ihgpwlah').find_longest_route()
        370
        >>> Rooms('kglvqrro').find_longest_route()
        492
        >>> Rooms('ulqzkmiv').find_longest_route()
        830
        """
        routes = [self.initial]
        longest = 0
        while routes:
            route = routes.pop()
            if self.is_vault(route):
                if len(route) > longest:
                    longest = len(route)
                continue

            for option in self.get_options(route):
                routes.append(option)

        return longest - len(self.initial)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(Rooms('awrkjxxr').find_shortest_route()))
    print("Part 2: {}".format(Rooms('awrkjxxr').find_longest_route()))
