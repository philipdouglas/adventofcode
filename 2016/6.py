def decode(lines, least_common=False):
    lines = [line.strip() for line in lines]
    col_counts = []
    for index in range(len(lines[0])):
        col_counts.append({})
    for line in lines:
        for index in range(len(col_counts)):
            col_counts[index].setdefault(line[index], 0)
            col_counts[index][line[index]] += 1

    message = ''
    for count in col_counts:
        sorted_chars = sorted(
            count.keys(), key=lambda letter: count[letter], reverse=True)
        message += sorted_chars[0] if not least_common else sorted_chars[-1]
    return message


if __name__ == "__main__":
    with open('6test.txt', 'r') as testfile:
        lines = testfile.readlines()
        print("Test 1: {}".format(decode(lines)))
        print("Test 2: {}".format(decode(lines, least_common=True)))
    with open('6input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        print("Part 1: {}".format(decode(lines)))
        print("Part 2: {}".format(decode(lines, least_common=True)))
