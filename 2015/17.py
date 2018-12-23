def count_combinations(nog, containers):
    """
    >>> count_combinations(25, [15, 10, 5, 5])
    (2, 1)
    >>> count_combinations(25, [20, 15, 10, 5, 5])
    (4, 3)
    """
    count = 0
    min_containers = None
    min_con_count = 0
    nodes = [[index] for index in range(len(containers))]
    while nodes:
        node = nodes.pop(0)
        total = sum(containers[index] for index in node)
        if total == nog:
            count += 1
            if min_containers is None or len(node) < min_containers:
                min_containers = len(node)
                min_con_count = 1
            elif len(node) == min_containers:
                min_con_count += 1
        if total >= nog:
            continue
        for remaining in range(node[-1] + 1, len(containers)):
            nodes.append(node + [remaining])
    return count, min_con_count


def adventofcode():
    with open('17.txt') as input_file:
        containers = [int(line) for line in input_file.readlines()]

    return count_combinations(150, containers)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
