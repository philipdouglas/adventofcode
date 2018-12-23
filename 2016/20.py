MAXIP = 4294967295


def merge_ranges(blocks, maxip=MAXIP):
    """
    >>> merge_ranges(((5, 8), (0, 2), (4, 7)), maxip=9)
    [[0, 2], [4, 8]]
    """
    previous = []
    consolidated = blocks
    while consolidated != previous:
        previous = sorted(consolidated)
        consolidated = []
        for low, high in previous:
            for index in range(len(consolidated)):
                low_match = low >= consolidated[index][0]
                high_match = high <= consolidated[index][1]
                if low_match and high_match:
                    break
                elif low_match and low <= consolidated[index][1] + 1:
                    consolidated[index][1] = high
                    break
                elif high_match and high >= consolidated[index][0] - 1:
                    consolidated[index][0] = low
                    break
            else:
                consolidated.append([low, high])
    return consolidated


def parse_input(filename):
    with open(filename, 'r') as inputfile:
        ranges = [line.strip().split('-') for line in inputfile.readlines()]
        return [(int(line[0]), int(line[1])) for line in ranges]


def count_ips(ranges, maxip=MAXIP):
    """
    >>> count_ips([[0, 2], [4, 8]], maxip=9)
    2
    """
    count = ranges[0][0]
    for index in range(len(ranges)):
        try:
            count += ranges[index + 1][0] - ranges[index][1] - 1
            # -1 because it's not inclusive 94 - 96 is one IP
            # print(f"{ranges[index]} -> {ranges[index + 1]} [{count}]")
        except IndexError:
            break
    count += maxip - ranges[-1][1]
    return count


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ranges = parse_input('20input.txt')
    merged = merge_ranges(ranges)
    print(f"Part 1: {merged[0][1] + 1}")
    print(f"Part 2: {count_ips(merged)}")
