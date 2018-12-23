defmodule Day19 do
  defp parse_char(char) do
    case char do
      "|" -> :forward
      "-" -> :forward
      "+" -> :turn
      char -> char
    end
  end

  def parse(input) do
    for {row, y} <- Enum.with_index(input),
        row = String.graphemes(row),
        {char, x} <- Enum.with_index(row),
        char != " ",
        do: {{x, y}, parse_char(char)},
        into: %{}
  end

  defp coord_add({x, y}, {m, n}), do: {x + m, y + n}

  defp walk(oldpos, map, direction \\ {0, 1}, route \\ [], steps \\ 1) do
    newpos = coord_add(oldpos, direction)
    case Map.get(map, newpos, nil) do
      nil ->
        {route |> Enum.reverse() |> Enum.join(), steps}

      :forward ->
        walk(newpos, map, direction, route, steps + 1)

      :turn ->
        [newdir] =
          for newdir <- [{-1, 0}, {0, -1}, {1, 0}, {0, 1}],
              next = coord_add(newpos, newdir),
              next != oldpos,
              Map.get(map, next, nil) != nil,
              do: newdir
        walk(newpos, map, newdir, route, steps + 1)

      letter ->
        walk(newpos, map, direction, [letter | route], steps + 1)
    end
  end

  def navigate(map) do
    for {x, y} <- Map.keys(map),
        y == 0,
        Map.get(map, {x, 0}, nil) != nil do
      walk({x, 0}, map)
    end
    |> Enum.at(0)
  end
end

ExUnit.start()
defmodule Day19Test do
  use ExUnit.Case

  test "part1" do
    input = [
      "     |          ",
      "     |  +--+    ",
      "     A  |  C    ",
      " F---|----E|--+ ",
      "     |  |  |  D ",
      "     +B-+  +--+ ",
    ]
    map = Day19.parse(input)
    assert Map.get(map, {0, 0}) == nil
    assert Map.get(map, {5, 0}) == :forward
    assert Map.get(map, {2, 3}) == :forward
    assert Map.get(map, {5, 2}) == "A"
    assert Map.get(map, {5, 5}) == :turn
    assert Day19.navigate(map) == {"ABCDEF", 38}
  end
end

with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 19), do: raw
|> String.split("\n", trim: true)
|> Day19.parse()
|> Day19.navigate()
|> IO.inspect()
