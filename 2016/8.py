import re


class Screen:
    def __init__(self, height=6, width=50):
        self.height = height
        self.width = width
        self.pixels = []
        for row in range(height):
            self.pixels.append([False] * width)

    def __str__(self):
        """
        >>> print(Screen(2, 4))
        ____
        ____
        """
        out = []
        for row in self.pixels:
            line = ''
            for pixel in row:
                line += '#' if pixel else '_'
            out.append(line)
        return '\n'.join(out)

    def rect(self, A, B):
        """
        >>> s = Screen(2, 6)
        >>> print(s.rect(1, 1))
        #_____
        ______
        >>> print(s.rect(4, 2))
        ####__
        ####__
        """
        for vert in range(B):
            for horz in range(A):
                self.pixels[vert][horz] = True
        return self

    def rotate_row(self, A, B):
        """
        >>> s = Screen(2, 6)
        >>> print(s.rect(3, 2))
        ###___
        ###___
        >>> print(s.rotate_row(0, 2))
        __###_
        ###___
        >>> print(s.rotate_row(1, 7))
        __###_
        _###__
        """
        B %= self.width
        self.pixels[A] = self.pixels[A][-B:] + self.pixels[A][:-B]
        return self

    def rotate_col(self, A, B):
        """
        >>> s = Screen(3, 6)
        >>> print(s.rect(3, 1))
        ###___
        ______
        ______
        >>> print(s.rotate_col(1, 2))
        #_#___
        ______
        _#____
        >>> print(s.rotate_col(1, 1))
        ###___
        ______
        ______
        >>> print(s.rotate_col(1, 12))
        ###___
        ______
        ______
        """
        for _ in range(B % self.height):
            prev = self.pixels[-1][A]
            for row in range(self.height):
                replacing = self.pixels[row][A]
                self.pixels[row][A] = prev
                prev = replacing
        return self

    def count(self):
        """
        >>> s = Screen(2, 6)
        >>> s.count()
        0
        >>> s.rect(3, 1).count()
        3
        """
        count = 0
        for row in self.pixels:
            for pixel in row:
                if pixel:
                    count += 1
        return count


    parse_re = re.compile(r'(?:(?:rotate )?(rect|row|column) (?:[xy]=)?(\d+)(?:x| by )(\d+))')

    def follow_instructions(self, lines):
        """
        >>> s = Screen(3, 7)
        >>> s.follow_instructions(['rect 3x2', 'rotate column x=1 by 1', 'rotate row y=0 by 4', 'rotate column x=1 by 1'])
        6
        """
        meth_map = {
            'rect': self.rect,
            'row': self.rotate_row,
            'column': self.rotate_col,
        }
        for line in lines:
            match = self.parse_re.match(line)
            meth_map[match.group(1)](int(match.group(2)), int(match.group(3)))
        return self.count()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('8input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        screen1 = Screen()
        print("Part 1: {}".format(screen1.follow_instructions(lines)))
        print(screen1)
