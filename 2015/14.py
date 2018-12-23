import re

regex = re.compile(
    r'([a-zA-Z]+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.')


def parse_line(line):
    """
    >>> parse_line('Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.')
    ('Comet', 14, 10, 127)
    """
    match = regex.match(line)
    return match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4))


def parse_lines(lines):
    for line in lines:
        yield parse_line(line)


def part1(lines):
    reindeers = {parsed[0]: parsed[1:] for parsed in parse_lines(lines)}
    furthest = 0
    for reindeer, stats in reindeers.items():
        speed, flight_time, rest_time = stats
        distance = (2503 // (flight_time + rest_time)) * (speed * flight_time)
        remainder = 2503 % (flight_time + rest_time)
        distance += min(flight_time, remainder) * speed
        if distance > furthest:
            furthest = distance
    return furthest


class Reindeer:
    def __init__(self, name, speed, flight_time, rest_time):
        self.name = name
        self.speed = speed
        self.flight_time = flight_time
        self.rest_time = rest_time

        self.distance = 0
        self.flying = True
        self.remaining = self.flight_time

        self.points = 0

    def tick(self):
        self.remaining -= 1
        if self.flying:
            self.distance += self.speed
        if self.remaining == 0:
            self.flying = not self.flying
            self.remaining = self.flight_time if self.flying else self.rest_time


def part2(lines):
    reindeers = [Reindeer(*parsed) for parsed in parse_lines(lines)]

    winner = reindeers[0]
    for second in range(2503):
        for reindeer in reindeers:
            reindeer.tick()
            if reindeer.distance > winner.distance:
                winner = reindeer
        winner.points += 1

    for reindeer in reindeers:
        if reindeer.points > winner.points:
            winner = reindeer
    return winner.points


def adventofcode():
    with open('14.txt') as input_file:
        lines = input_file.readlines()

    return part1(lines), part2(lines)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
