from computer import TogglePuter


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('23test.txt', 'r') as testfile:
        lines = testfile.readlines()
        test1 = TogglePuter()
        test1.run(lines, debug=False)
        print("Test 1: {}".format(test1.a))

    with open('23input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        part1 = TogglePuter()
        part1.a = 7
        part1.run(lines, debug=False)
        print("Part 1: {}".format(part1.a))

        part2 = TogglePuter()
        part2.a = 12
        part2.run(lines, debug=False)
        print("Part 2: {}".format(part2.a))
