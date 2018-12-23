import functools
import itertools
import operator


def quantumn_entanglement(packages):
    """
    >>> quantumn_entanglement([11, 9])
    99
    >>> quantumn_entanglement([10, 9, 1])
    90
    >>> quantumn_entanglement([10, 8, 2])
    160
    >>> quantumn_entanglement([10, 7, 3])
    210
    >>> quantumn_entanglement([10, 5, 4, 1])
    200
    """
    return functools.reduce(operator.mul, packages)


def assignments(length, number):
    assignment = [0] * length
    while True:
        index = -1
        try:
            while assignment[index] == (number - 1):
                assignment[index] = 0
                index -= 1
            assignment[index] += 1
            yield assignment
        except IndexError:
            break


def generate_groups(packages):
    target = sum(packages) // 3
    for assignment in assignments(len(packages), 3):
        totals = [0, 0, 0]
        groups = [[], [], []]
        for index in range(len(packages)):
            totals[assignment[index]] += packages[index]
            if totals[assignment[index]] > target:
                break
            groups[assignment[index]].append(packages[index])
        else:
            yield groups


def adventofcode():
    with open('24.txt') as input_file:
        packages = [int(line) for line in input_file.readlines() if line.strip()]

    least = None
    least_qe = None
    for groups in generate_groups(packages):
        for group in groups:
            if least is None or len(group) < least:
                least = len(group)
                print(least)
                least_qe = quantumn_entanglement(group)
                print("qe: {}".format(least_qe))
            elif len(group) == least:
                new_qe = quantumn_entanglement(group)
                if new_qe < least_qe:
                    least_qe = new_qe
                    print("qe: {}".format(least_qe))
    return least_qe


def check_sum(packages, cur_parts, target, parts):
    "Stolen from https://www.reddit.com/r/adventofcode/comments/3y1s7f/day_24_solutions/cy9srkh"
    for group_size in range(len(packages)):
        for combination in itertools.combinations(packages, group_size):
            if sum(combination) == target:
                if cur_parts == 2:
                    return True
                elif cur_parts < parts:
                    return check_sum(list(set(packages) - set(combination)), cur_parts - 1, target, parts)
                elif check_sum(list(set(packages) - set(combination)), cur_parts - 1, target, parts):
                    return quantumn_entanglement(combination)


def adventofcodefast(parts=3):
    with open('24.txt') as input_file:
        packages = [int(line) for line in input_file.readlines() if line.strip()]

    target = sum(packages) // parts
    return check_sum(packages, parts, target, parts)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcodefast())
    print(adventofcodefast(4))
