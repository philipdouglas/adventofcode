weapons = {
    'dagger': (8, 4),
    'shortsword': (10, 5),
    'warhammer': (25, 6),
    'longsword': (40, 7),
    'greataxe': (74, 8),
}

armours = {
    'none': (0, 0),
    'leather': (13, 1),
    'chainmail': (31, 2),
    'splintmail': (53, 3),
    'bandedmail': (75, 4),
    'platemail': (102, 5),
}

rings = {
    'none': (0, 0, 0),
    'none2': (0, 0, 0),
    'damage +1': (25, 1, 0),
    'damage +2': (50, 2, 0),
    'damage +3': (100, 3, 0),
    'defense +1': (20, 0, 1),
    'defense +2': (40, 0, 2),
    'defense +3': (80, 0, 3),
}


class Victory(Exception):
    def __init__(self, character):
        self.character = character


class Character:
    """
    >>> p = Character(100, 0, 0)
    >>> p.armour = (23, 6)
    >>> p.hp
    100
    >>> p.arm
    6
    >>> p.spent
    23
    >>> p.weapon = (23, 6)
    >>> p.dmg
    6
    >>> p.spent
    46
    >>> p.ring = (23, 6, 3)
    >>> p.dmg
    12
    >>> p.arm
    9
    >>> p.spent
    69
    """
    def __init__(self, hp, dmg, arm):
        self.hp = hp
        self.dmg = dmg
        self.arm = arm
        self._armour = None
        self._weapon = None
        self._rings = []
        self.spent = 0

    @property
    def armour(self):
        return self._armour

    @armour.setter
    def armour(self, armour):
        cost, rating = armour
        self.spent += cost
        self.arm += rating

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, weapon):
        cost, rating = weapon
        self.spent += cost
        self.dmg += rating

    @property
    def ring(self):
        return self._rings

    @ring.setter
    def ring(self, ring):
        cost, dmg, arm = ring
        self.spent += cost
        self.dmg += dmg
        self.arm += arm
        self._rings.append(ring)

    def attack(self, character):
        """
        >>> b = Character(12, 7, 2)
        >>> p = Character(8, 5, 5)
        >>> p.attack(b)
        >>> b.hp
        9
        >>> b.attack(p)
        >>> p.hp
        6
        """
        character.hp -= max(self.dmg - character.arm, 1)
        if character.hp <= 0:
            raise Victory(self)

    def __str__(self):
        return "HP: {} D: {} A: {}".format(self.hp, self.dmg, self.arm)


def fight(boss, player):
    """
    >>> b = Character(12, 7, 2)
    >>> p = Character(8, 5, 5)
    >>> v = fight(b, p)
    >>> v == p
    True
    >>> b = Character(12, 9, 2)
    >>> p = Character(8, 5, 5)
    >>> v = fight(b, p)
    >>> v == b
    True
    """
    order = (player, boss)
    try:
        while True:
            player.attack(boss)
            boss.attack(player)
    except Victory as victor:
        return victor.character


def adventofcode():
    cheapest = None
    expensiveist = 0
    for wname, weapon in weapons.items():
        for aname, armour in armours.items():
            for r1name, ring1 in rings.items():
                for r2name, ring2 in rings.items():
                    if r1name == r2name:
                        continue
                    boss = Character(104, 8, 1)
                    player = Character(100, 0, 0)
                    player.weapon = weapon
                    player.armour = armour
                    player.ring = ring1
                    player.ring = ring2

                    victor = fight(boss, player)
                    # print("a: {} w: {} r1: {} r2: {} c: {}".format(aname, wname, r1name, r2name, player.spent))
                    # print(player)
                    if victor == player:
                        # print("Player wins!")
                        if cheapest is None or cheapest > victor.spent:
                            cheapest = victor.spent
                            # print(cheapest)
                    else:
                        if expensiveist < player.spent:
                            expensiveist = player.spent
    return cheapest, expensiveist



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())