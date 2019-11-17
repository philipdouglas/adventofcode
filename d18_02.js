"use strict";
const assert = require("assert").strict;

function parseInput(input) {
  return input.split("\n");
}

// Part 1
// ======

function check_id(id) {
  const counts = {};
  for (const char of id) {
    counts[char] = (counts[char] || 0) + 1;
  }
  const values = new Set(Object.values(counts));
  return [values.has(2), values.has(3)]
}

function checksum(ids) {
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
  return checksum(parseInput(input));
};

// Part 2
// ======

const part2 = input => {
  return input;
};

module.exports = { part1, part2 };
