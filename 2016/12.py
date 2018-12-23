from computer import Computer


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('12input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        part1 = Computer()
        part1.run(lines)
        print("Part 1: {}".format(part1.a))
        part2 = Computer()
        part2.c = 1
        part2.run(lines)
        print("Part 1: {}".format(part2.a))
