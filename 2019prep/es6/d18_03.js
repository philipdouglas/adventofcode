"use strict";
const assert = require("assert").strict;

const parse_input = input => {
  return input.split("\n");
};

// Part 1
// ======
class Coord {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  add(other) {
    return new Coord(this.x + other.x, this.y + other.y);
  }

  add(other) {
    return new Coord(this.x + other.x, this.y + other.y);
  }

  gte(other) {
    return this.x >= other.x && this.y >= other.y;
  }

  lte(other) {
    return this.x <= other.x && this.y <= other.y;
  }

  toString() {
    return `${this.x},${this.y}`
  }
}

class Claim {
  constructor(id, start, size) {
    this.id = id;
    this.start = start;
    this.end = start.add(size);
  }

  contains(point) {
    return point.gte(this.start) && point.lte(this.end);
  }
}

const claim_re = /#(\d+) @ (\d+),(\d+): (\d+)x(\d)+/

const parse_claim = line => {
  const parts = claim_re.exec(line);
  return new Claim(
    parts[1],
    new Coord(Number(parts[2]), Number(parts[3])),
    new Coord(Number(parts[4]), Number(parts[5])))
}

const find_overlaps = lines => {
  const fabric = {};
  for (const claim of lines.map(parse_claim)) {
    for (let x = claim.start.x; x < claim.end.x; x++) {
      for (let y = claim.start.y; y < claim.end.y; y++) {
        const point = new Coord(x, y);
        if (!fabric[point]) fabric[point] = [];
        fabric[point].push(claim.id);
      }
    }
  }
  return Object.values(fabric).filter(ids => ids.length > 1).length;
}

const part1 = input => {
  assert.strictEqual(
    find_overlaps(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"]),
    4
  );
  assert.strictEqual(
    find_overlaps(["#1 @ 1,3: 4x4", "#2 @ 2,1: 4x4", "#3 @ 5,5: 2x2"]),
    6
  );
  assert.strictEqual(
    find_overlaps([
      "#1 @ 1,3: 4x4",
      "#2 @ 2,1: 4x4",
      "#3 @ 5,5: 2x2",
      "#4 @ 1,3: 1x1"
    ]),
    7
  );
  assert.strictEqual(
    find_overlaps(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2", "#4 @ 0,0: 7x7"]),
    32
  );
  return find_overlaps(parse_input(input));
};

// Part 2
// ======

const part2 = input => {
  return input;
};

module.exports = { part1, part2 };
