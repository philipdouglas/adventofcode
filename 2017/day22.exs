defmodule Day22 do
  defp parse_cell(cell) do
    case cell do
      "." -> false
      "#" -> true
    end
  end

  def parse(input) do
    lines = input |> String.split("\n", trim: true)
    offset = lines |> length() |> div(2)
    for {line, y} <- Enum.with_index(lines),
        {cell, x} <- String.graphemes(line) |> Enum.with_index(),
        do: {{x - offset, offset - y}, parse_cell(cell)},
        into: %{}
  end

  def left({x, y}), do: {-y, x}
  def right({x, y}), do: {y, -x}
  def reverse({x, y}), do: {-x, -y}
  def move({x, y}, {dx, dy}), do: {x + dx, y + dy}

  def burst(_, {count, mem, pos, direction}) do
    current = Map.get(mem, pos, false)
    direction = if current, do: right(direction), else: left(direction)
    mem = Map.put(mem, pos, !current)
    pos = move(pos, direction)
    count = count + if !current, do: 1, else: 0
    {count, mem, pos, direction}
  end

  def part1(mem, num) do
    1..num
    |> Enum.reduce({0, mem, {0, 0}, {0, 1}}, &burst/2)
    |> elem(0)
  end

  def burst2(_, {count, mem, pos, direction}) do
    current = Map.get(mem, pos, false)
    direction = case current do
      false -> left(direction)
      :weak -> direction
      true  -> right(direction)
      :flag -> reverse(direction)
    end
    mem = Map.put(mem, pos, case current do
      false -> :weak
      :weak -> true
      true  -> :flag
      :flag -> false
    end)
    pos = move(pos, direction)
    count = count + if current == :weak, do: 1, else: 0
    {count, mem, pos, direction}
  end

  def part2(mem, num) do
    1..num
    |> Enum.reduce({0, mem, {0, 0}, {0, 1}}, &burst2/2)
    |> elem(0)
  end
end

ExUnit.start()
defmodule Day22Test do
  use ExUnit.Case

  test "parse" do
    input = "..#\n#..\n...\n"
    assert Day22.parse(input) == %{
      {-1,  1} => false, { 0,  1} => false, { 1,  1} => true ,
      {-1,  0} => true , { 0,  0} => false, { 1,  0} => false,
      {-1, -1} => false, { 0, -1} => false, { 1, -1} => false,
    }
  end

  test "part1" do
    input = "..#\n#..\n...\n" |> Day22.parse()
    assert Day22.part1(input, 7) == 5
    assert Day22.part1(input, 70) == 41
    assert Day22.part1(input, 10000) == 5587
  end

  test "part2" do
    input = "..#\n#..\n...\n" |> Day22.parse()
    assert Day22.part2(input, 100) == 26
    assert Day22.part2(input, 10000000) == 2511944
  end
end

mem =
  with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 22), do: raw
  |> Day22.parse()

mem |> Day22.part1(10000) |> IO.puts()
mem |> Day22.part2(10000000) |> IO.puts()
