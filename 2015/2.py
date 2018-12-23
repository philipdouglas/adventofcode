import operator
from functools import reduce


def surface_area(length, width, height):
	"""
	>>> surface_area(2, 3, 4)
	52
	>>> surface_area(1, 1, 10)
	42"""
	return (2 * length * width) + (2 * width * height) + (2 * height * length)

def calc_paper(box):
	"""
	>>> calc_paper((2, 3, 4))
	58
	>>> calc_paper((1, 1, 10))
	43"""
	return surface_area(*box) + (box[0] * box[1])

def calc_ribbon(box):
	"""
	>>> calc_ribbon((2, 3, 4))
	34
	>>> calc_ribbon((1, 1, 10))
	14"""
	return (2 *(box[0] + box[1])) + reduce(operator.mul, box)


def adventofcode():
	with open('2.txt') as input_file:
		boxes = [sorted(int(dim) for dim in line.strip().split('x')) for line in input_file]

	paper = 0
	ribbon = 0
	for box in boxes:
		paper += calc_paper(box)
		ribbon += calc_ribbon(box)
	return paper, ribbon

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
