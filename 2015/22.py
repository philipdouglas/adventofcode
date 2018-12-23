from copy import deepcopy


class Victory(Exception):
    def __init__(self, character):
        self.character = character


class EndEffect(Exception):
    pass


class OutOfMana(Exception):
    pass


class Effect:
    duration = None

    def __init__(self, player, boss):
        self.remaining = self.duration

    def turn(self, player, boss):
        self.effect(player, boss)
        self.remaining -= 1
        if self.remaining <= 0:
            raise EndEffect

    def effect(self, player, boss):
        raise NotImplemented


class ShieldEffect(Effect):
    duration = 6

    def __init__(self, player, boss):
        super().__init__(player, boss)
        player.arm += 7

    def effect(self, player, boss):
        if self.remaining == 1:
            player.arm -= 7


class PoisonEffect(Effect):
    duration = 6

    def effect(self, player, boss):
        boss.hp -= 3


class RechargeEffect(Effect):
    duration = 5

    def effect(self, player, boss):
        player.gain_mana(101)


def magic_missile(player, boss):
    player.spend_mana(53)
    boss.hp -= 4


def drain(player, boss):
    player.spend_mana(73)
    boss.hp -= 2
    player.hp +=2


def shield(player, boss):
    player.spend_mana(113)
    return 'shield', ShieldEffect(player, boss)


def poison(player, boss):
    player.spend_mana(173)
    return 'poison', PoisonEffect(player, boss)


def recharge(player, boss):
    player.spend_mana(229)
    return 'recharge', RechargeEffect(player, boss)


SPELLS = [
    magic_missile,
    drain,
    shield,
    poison,
    recharge,
]


class Character:
    def __init__(self, hp, dmg, arm):
        self.hp = hp
        self.dmg = dmg
        self.arm = arm

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


class Player(Character):
    def __init__(self, hp, mana):
        super().__init__(hp, 0, 0)
        self._mana = mana
        self.mana_spent = 0
        self.effects = {}
        self.spells_cast = []

    def spend_mana(self, amount):
        self._mana -= amount
        self.mana_spent += amount
        if self._mana <= 0:
            raise OutOfMana

    def gain_mana(self, amount):
        self._mana += amount

    def cast(self, spell, boss):
        self.spells_cast.append(spell.__name__)
        effect = spell(self, boss)
        if boss.hp <= 0:
            raise Victory(self)
        if effect:
            name, effect = effect
            self.effects[name] = effect

    def resolve_effects(self, boss):
        finished = []
        for name, effect in self.effects.items():
            try:
                effect.turn(self, boss)
            except EndEffect:
                finished.append(name)
            if boss.hp <= 0:
                raise Victory(self)
        for name in finished:
            del self.effects[name]

    def __str__(self):
        return "HP: {} M: {} A: {}".format(self.hp, self._mana, self.arm)


def adventofcode():
    boss = Character(71, 10, 0)
    player = Player(50, 500)

    turns = [(player, boss)]
    lowest = None
    while turns:
        player, boss = turns.pop(0)

        for spell in SPELLS:
            if spell.__name__ in player.effects:
                # print("Can't cast")
                continue
            # print(spell.__name__)
            pclone = deepcopy(player)
            bclone = deepcopy(boss)
            try:
                pclone.cast(spell, bclone)
                pclone.resolve_effects(bclone)
                bclone.attack(pclone)
                pclone.hp -= 1
                if pclone.hp <= 0:
                    continue
                pclone.resolve_effects(bclone)
                # print(pclone)
                # print(bclone)
                turns.insert(0, (pclone, bclone))
            except OutOfMana:
                # print("OutOfMana")
                pass
            except Victory as victory:
                # print("Victory! {}".format(victory.character.__class__.__name__))
                if victory.character == pclone and (lowest is None or pclone.mana_spent < lowest):
                    lowest = pclone.mana_spent
                    print(lowest)
                    print(pclone.spells_cast)
    return lowest


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
