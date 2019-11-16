'use strict'
const assert = require("assert").strict;

function parseInput(input) {
  return input.split('\n').map(Number);
}

// Part 1
// ======

function apply_freq(shifts) {
  return shifts.reduce((a, b) => a + b);
}

const part1 = input => {
  assert(apply_freq([1, 1, 1]) == 3);
  assert(apply_freq([1, 1, -2]) == 0);
  assert(apply_freq([-1, -2, -3]) == -6);
  return apply_freq(parseInput(input));
}

// Part 2
// ======

const part2 = input => {
  return input;
}

module.exports = { part1, part2 }
