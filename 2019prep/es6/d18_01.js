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

function find_repeat(shifts) {
  const seen_values = new Set([0]);
  let current_value = 0;
  while (true) {
    for (const shift of shifts) {
      current_value += shift;
      if (seen_values.has(current_value)) {
        return current_value;
      }
      seen_values.add(current_value);
    }
  }
}

const part2 = input => {
  assert(find_repeat([1, -1]) === 0);
  assert(find_repeat([+3, +3, +4, -2, -4]) == 10);
  assert(find_repeat([-6, +3, +8, +5, -6]) == 5);
  assert(find_repeat([+7, +7, -2, -7, -4]) == 14);
  return find_repeat(parseInput(input));
}

module.exports = { part1, part2 }
