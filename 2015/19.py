import re
import string

class Replacement:
    """
    >>> h = Replacement('H')
    >>> h.add_replacement('HO')
    >>> h.add_replacement('OH')
    >>> sorted(list(h.do_replacements('HOH')))
    ['HOHO', 'HOOH', 'OHOH']
    >>> o = Replacement('O')
    >>> o.add_replacement('HH')
    >>> sorted(list(o.do_replacements('HOH')))
    ['HHHH']
    """
    def __init__(self, matches):
        self.pattern = re.compile(matches)
        self.replacements = []

    def add_replacement(self, replacement):
        self.replacements.append(replacement)

    def do_replacements(self, molecule):
        new_molecules = set()
        for match in self.pattern.finditer(molecule):
            for replacement in self.replacements:
                new_molecules.add(molecule[:match.start()] + replacement + molecule[match.end():])
        return new_molecules



def find_molecule(molecule, replacements):
    """
    >>> replacements = {'H': 'e', 'O': 'e', 'HO': 'H', 'OH': 'H', 'HH': 'O'}
    >>> find_molecule('HOH', replacements)
    3
    >>> find_molecule('HOHOHO', replacements)
    6
    """
    count = 0
    sorted_thises = sorted(replacements.keys(), key=len, reverse=True)
    while molecule != 'e':
        for this in sorted_thises:
            if this in molecule:
                molecule = molecule.replace(this, replacements[this], 1)
                count += 1
                break
        else:
            raise Exception("stuck")
    return count


def adventofcode():
    molecule = None
    replacement_inputs = []
    with open('19.txt') as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if '=>' in line:
                replacement_inputs.append(line)
            elif line:
                molecule = line

    replacements = {}
    for replacement_input in replacement_inputs:
        pattern, replacement = replacement_input.split(' => ')
        if pattern not in replacements:
            replacements[pattern] = Replacement(pattern)
        replacements[pattern].add_replacement(replacement)


def adventofcodeday2():
    molecule = None
    replacement_inputs = []
    with open('19.txt') as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if '=>' in line:
                replacement_inputs.append(line)
            elif line:
                molecule = line

    replacements = {}
    for replacement_input in replacement_inputs:
        pattern, replacement = replacement_input.split(' => ')
        replacements[replacement] = pattern

    return find_molecule(molecule, replacements)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
    print(adventofcodeday2())
