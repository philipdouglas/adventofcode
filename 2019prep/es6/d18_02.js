"use strict";
const assert = require("assert").strict;

const parse_input = (input) => {
  return input.split("\n");
}

// Part 1
// ======

const check_id = (id) => {
  const counts = {};
  for (const char of id) {
    counts[char] = (counts[char] || 0) + 1;
  }
  const values = new Set(Object.values(counts));
  return [values.has(2), values.has(3)]
}

const checksum = (ids) => {
  const [twos, threes] = ids.map(check_id).reduce((
    [twos, threes], [two, three]) => [twos + Number(two), threes + Number(three)]
  );
  return twos * threes;
}

const part1 = input => {
  assert.deepStrictEqual(check_id("abcdef"), [false, false]);
  assert.deepStrictEqual(check_id("bababc"), [true, true]);
  assert.deepStrictEqual(check_id("abbcde"), [true, false]);
  assert.deepStrictEqual(check_id("abcccd"), [false, true]);
  assert.deepStrictEqual(check_id("aabcdd"), [true, false]);
  assert.deepStrictEqual(check_id("abcdee"), [true, false]);
  assert.deepStrictEqual(check_id("ababab"), [false, true]);
  assert.strictEqual(checksum([
    "abcdef",
    "bababc",
    "abbcde",
    "abcccd",
    "aabcdd",
    "abcdee",
    "ababab",
  ]), 12)
  return checksum(parse_input(input));
};

// Part 2
// ======

const compare_ids = (a, b) => {
  const similar = a.split('').filter((char, index) => char == b[index]);
  if (similar.length == a.length - 1) {
    return similar.join('');
  }
  return false;
}

const find_box = (ids) => {
  for (const first of ids) {
    for (const second of ids) {
      const similarity = compare_ids(first, second);
      if (similarity) {
        return similarity;
      }
    }
  }
}

const part2 = input => {
  assert.strictEqual(compare_ids("abcde", "axcye"), false);
  assert.strictEqual(compare_ids("fghij", "fguij"), "fgij");
  assert.strictEqual(find_box([
    "abcde",
    "fghij",
    "klmno",
    "pqrst",
    "fguij",
    "axcye",
    "wvxyz",
  ]), 'fgij')
  return find_box(parse_input(input));
};

module.exports = { part1, part2 };
