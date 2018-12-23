import sequtils
import strutils
import sugar
from unittest import check

let input = strip(readFile("2017/.cache/input_2017_1"))
var digits: seq[int] = input.map((digit) => parseInt($digit))

proc captcha(digits: seq[int], offset: int = 0): int =
    var offset = offset
    if offset == 0:
        offset = digits.len div 2
    for index, digit in digits:
        if digit == digits[(index + offset) mod digits.len]:
            result += digit

check:
    captcha(@[1, 1, 2, 2], 1) == 3
    captcha(@[1, 1, 1, 1], 1) == 4
    captcha(@[1, 2, 3, 4], 1) == 0
    captcha(@[9, 1, 2, 1, 2, 1, 2, 9], 1) == 9

    captcha(@[1, 2, 1, 2]) == 6
    captcha(@[1, 2, 2, 1]) == 0
    captcha(@[1, 2, 3, 4, 2, 5]) == 4
    captcha(@[1, 2, 3, 1, 2, 3]) == 12
    captcha(@[1, 2, 1, 3, 1, 4, 1, 5]) == 4

echo captcha(digits, 1)
echo captcha(digits)
