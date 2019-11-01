import algorithm
import sequtils
import strutils
import sugar
from unittest import check

let input = readFile("2017/.cache/input_2017_4").strip.split('\n')

proc isValid(pass: string): bool =
    let words = pass.split(' ')
    return words == deduplicate(words)

proc testPasswords(passwords: openArray[string], check: (string) -> bool): int =
    for password in passwords:
        if check(password):
            result += 1

proc isSuperValid(pass: string): bool =
    let words = pass.split(' ')
    return words.len == words.map((word) => sorted(word, cmp)).deduplicate.len

check:
    isValid("aa bb cc dd ee") == true
    isValid("aa bb cc dd aa") == false
    isValid("aa bb cc dd aaa") == true

    isSuperValid("abcde fghij") == true
    isSuperValid("abcde xyz ecdab") == false
    isSuperValid("a ab abc abd abf abj") == true
    isSuperValid("iiii oiii ooii oooi oooo") == true
    isSuperValid("oiii ioii iioi iiio") == false

echo testPasswords(input, isValid)
echo testPasswords(input, isSuperValid)
