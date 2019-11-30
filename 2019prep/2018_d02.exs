defmodule Day1 do
  def counts(box) do
    counts = box
    |> String.graphemes
    |> Enum.sort
    |> Enum.group_by(fn(char) -> char end)
    |> Map.values
    |> Enum.map(&Enum.count/1)
    [Enum.member?(counts, 2), Enum.member?(counts, 3)]
  end

  def part1(boxes) do
    counts = boxes |> Enum.map(&Day1.counts/1)
    twos = counts |> Enum.filter(fn ([two, _]) -> two end) |> Enum.count
    threes = counts |> Enum.filter(fn ([_, three]) -> three end) |> Enum.count
    twos * threes
  end

  def part2(boxes) do
  end
end

ExUnit.start

defmodule Day1Test do
  use ExUnit.Case

  test "part1" do
    boxes = [
      "abcdef",
      "bababc",
      "abbcde",
      "abcccd",
      "aabcdd",
      "abcdee",
      "ababab",
    ]
    assert boxes |> Day1.part1() == 12
  end

  test "part2" do

  end
end

input = with {:ok, raw} = AdventOfCodeHelper.get_input(2018, 2), do: raw
|> String.trim()
|> String.split("\n")

input
|> Day1.part1
|> IO.puts()

input
|> Day1.part2
|> IO.puts()
