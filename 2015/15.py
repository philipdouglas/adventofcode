import copy


class Ingredient:
    """
    >>> b = Ingredient(-1, -2, 6, 3, 8)
    >>> b
    Ingredient: capacity -1, durability -2, flavor 6, texture 3, calories 8
    >>> b = b * 44
    >>> b
    Ingredient: capacity -44, durability -88, flavor 264, texture 132, calories 352
    >>> c = Ingredient(2, 3, -2, -1, 3)
    >>> c
    Ingredient: capacity 2, durability 3, flavor -2, texture -1, calories 3
    >>> c = c * 56
    >>> c
    Ingredient: capacity 112, durability 168, flavor -112, texture -56, calories 168
    >>> bc = b + c
    >>> bc
    Ingredient: capacity 68, durability 80, flavor 152, texture 76, calories 520
    >>> bc.score
    62842880
    """
    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    calories = 0

    def __repr__(self):
        return "{}: capacity {}, durability {}, flavor {}, texture {}, calories {}".format(
            self.__class__.__name__, self.capacity, self.durability, self.flavor, self.texture,
            self.calories)

    def __init__(self, capacity, durability, flavor, texture, calories):
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories
        self.score = max(0, self.capacity) * max(0, self.durability) * max(0, self.flavor) * max(0, self.texture)

    def __mul__(self, other):
        return Ingredient(
            self.capacity * other,
            self.durability * other,
            self.flavor * other,
            self.texture * other,
            self.calories * other,
        )

    def __add__(self, other):
        return Ingredient(
            self.capacity + other.capacity,
            self.durability + other.durability,
            self.flavor + other.flavor,
            self.texture + other.texture,
            self.calories + other.calories,
        )


frosting = Ingredient(4, -2, 0, 0, 5)
candy = Ingredient(0, 5, -1, 0, 8)
butterscotch = Ingredient(-1, 0, 5, 0, 6)
sugar = Ingredient(0, 0, -2, 2, 1)


def combinations():
    for zero in range(0, 101):
        for one in range(0, 101):
            for two in range(0, 101):
                for three in range(0, 101):
                    combination = [zero, one, two, three]
                    if sum(combination) == 100:
                        yield combination


def adventofcode():
    highest = 0
    highest_lite = 0
    for combination in combinations():
        cookie = (
            (frosting * combination[0]) +
            (candy * combination[1]) +
            (butterscotch * combination[2]) +
            (sugar * combination[3])
        )
        if cookie.score > highest:
            highest = cookie.score
        if cookie.calories == 500 and cookie.score > highest_lite:
            highest_lite = cookie.score
    return highest, highest_lite


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
