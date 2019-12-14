
import collections
from math import ceil

from aocd.models import Puzzle

from util import inspect


def parse(lines):
    """
    >>> parse(["10 ORE => 10 A"])
    {'A': (10, [('ORE', 10)])}
    >>> parse(["10 ORE, 3 B => 10 A"])
    {'A': (10, [('ORE', 10), ('B', 3)])}
    """
    tree = {}
    for line in lines:
        inp, out = line.split(' => ')
        inputs = (req.split(' ') for req in inp.split(', '))
        amount, material = out.split(' ')
        tree[material] = (int(amount), [
            (material, int(amount)) for amount, material in inputs
        ])
    return tree


def compute_depths(tree):
    stack = [('FUEL', 0)]
    depths = {}
    while stack:
        mat, depth = stack.pop()
        depths[mat] = max(depth, depths.get(mat, 0))
        try:
            _, mats = tree[mat]
            for new_mat, _ in mats:
                stack.append((new_mat, depth + 1))
        except KeyError:
            pass
    return depths


def produce_fuel(fuel, tree, depths):
    ore = 0
    requirements = collections.Counter(FUEL=fuel)
    surplus = {}
    while requirements:
        material = sorted(requirements.keys(), key=lambda req: depths[req])[0]
        needed = requirements[material]
        del requirements[material]
        if material in surplus:
            needed -= surplus[material]
            if needed >= 0:
                surplus[material] == 0
            else:
                surplus[material] = -needed
        if needed <= 0:
            continue
        elif material == 'ORE':
            ore += needed
        else:
            number_made, new_reqs = tree[material]
            multiples_needed = ceil(needed / number_made)
            if number_made > needed:
                surplus[material] = surplus.get(material, 0) + number_made - needed
            for material, amount in new_reqs:
                requirements[material] += amount * multiples_needed
    return ore


def part1(lines):
    """
    >>> part1(["10 ORE => 10 A", "1 ORE => 1 B", "7 A, 1 B => 1 C", "7 A, 1 C => 1 D", "7 A, 1 D => 1 E", "7 A, 1 E => 1 FUEL"])
    31
    >>> part1(["9 ORE => 2 A", "8 ORE => 3 B", "7 ORE => 5 C", "3 A, 4 B => 1 AB", "5 B, 7 C => 1 BC", "4 C, 1 A => 1 CA", "2 AB, 3 BC, 4 CA => 1 FUEL", ])
    165
    >>> part1(["157 ORE => 5 NZVS", "165 ORE => 6 DCFZ", "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL", "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", "179 ORE => 7 PSHF", "177 ORE => 5 HKGWZ", "7 DCFZ, 7 PSHF => 2 XJWVT", "165 ORE => 2 GPVTF", "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT", ])
    13312
    >>> part1(["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG","17 NVRVD, 3 JNWZP => 8 VPVL","53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL","22 VJHF, 37 MNCFX => 5 FWMGM","139 ORE => 4 NVRVD","144 ORE => 7 JNWZP","5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC","5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV","145 ORE => 6 MNCFX","1 NVRVD => 8 CXFTF","1 VJHF, 6 MNCFX => 4 RFSQX","176 ORE => 6 VJHF",])
    180697
    >>> part1(["171 ORE => 8 CNZTR", "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL", "114 ORE => 4 BHXH", "14 VRPVC => 6 BMBT", "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL", "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT", "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW", "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", "5 BMBT => 4 WPTQ", "189 ORE => 9 KTJDG", "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", "12 VRPVC, 27 CNZTR => 2 XDBXC", "15 KTJDG, 12 BHXH => 5 XCVML", "3 BHXH, 2 VRPVC => 7 MZWV", "121 ORE => 7 VRPVC", "7 XCVML => 6 RJRHP", "5 BHXH, 4 VRPVC => 5 LTCX", ])
    2210736
    """
    tree = parse(lines)
    depths = compute_depths(tree)
    return produce_fuel(1, tree, depths)


def part2(lines):
    """
    >>> part2(["157 ORE => 5 NZVS", "165 ORE => 6 DCFZ", "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL", "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", "179 ORE => 7 PSHF", "177 ORE => 5 HKGWZ", "7 DCFZ, 7 PSHF => 2 XJWVT", "165 ORE => 2 GPVTF", "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT", ])
    82892753
    >>> part2(["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG","17 NVRVD, 3 JNWZP => 8 VPVL","53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL","22 VJHF, 37 MNCFX => 5 FWMGM","139 ORE => 4 NVRVD","144 ORE => 7 JNWZP","5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC","5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV","145 ORE => 6 MNCFX","1 NVRVD => 8 CXFTF","1 VJHF, 6 MNCFX => 4 RFSQX","176 ORE => 6 VJHF",])
    5586022
    >>> part2(["171 ORE => 8 CNZTR", "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL", "114 ORE => 4 BHXH", "14 VRPVC => 6 BMBT", "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL", "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT", "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW", "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", "5 BMBT => 4 WPTQ", "189 ORE => 9 KTJDG", "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", "12 VRPVC, 27 CNZTR => 2 XDBXC", "15 KTJDG, 12 BHXH => 5 XCVML", "3 BHXH, 2 VRPVC => 7 MZWV", "121 ORE => 7 VRPVC", "7 XCVML => 6 RJRHP", "5 BHXH, 4 VRPVC => 5 LTCX", ])
    460664
    """
    tree = parse(lines)
    depths = compute_depths(tree)
    lower_bound = 0
    upper_bound = 100000000
    while upper_bound - lower_bound > 1:
        middle = lower_bound + ((upper_bound - lower_bound) // 2)
        ore_used = produce_fuel(middle, tree, depths)
        if ore_used <= 1000000000000:
            lower_bound = middle
        else:
            upper_bound = middle
    return lower_bound


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=14)
    lines = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(lines), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(lines), prefix='Part 2: ')
