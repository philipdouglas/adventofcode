defmodule Day24 do
  def parse(input) do
    for component <- input do
      for port <- String.split(component, "/") do
        String.to_integer(port)
      end
    end
    |> Enum.flat_map(&([&1, Enum.reverse(&1)]))
    |> Enum.map(&List.to_tuple/1)
    |> Enum.reduce(%{}, fn({a, b}, map) ->
      Map.put(map, a, [b | Map.get(map, a, [])])
    end)
  end

  def bridges(map, sofar \\ [0])
  def bridges(map, [current | sofar]) do
    recurse =
      Map.get(map, current)
      |> Enum.flat_map(fn(next) ->
        map = Map.put(map, current, Map.get(map, current) |> List.delete(next))
        map = Map.put(map, next, Map.get(map, next) |> List.delete(current))
        bridges(map, [next, current, current | sofar])
      end)
    [[current | sofar] | recurse ]
  end

  def strongest(bridges) do
    bridges
    |> Enum.map(&Enum.sum/1)
    |> Enum.max()
  end

  def strongest_longest(bridges) do
    bridges
    |> Enum.sort_by(&Enum.sum/1)
    |> Enum.sort_by(&length/1)
    |> Enum.at(-1)
    |> Enum.sum()
  end
end

ExUnit.start()
defmodule Day24Test do
  use ExUnit.Case

  test "parse" do
    input = ["0/2", "2/2", "2/3", "3/4", "3/5", "0/1", "10/1", "9/10"]
    assert Day24.parse(input) == %{
      0 => [1, 2],
      1 => [10, 0],
      2 => [3, 2, 2, 0],
      3 => [5, 4, 2],
      4 => [3],
      5 => [3],
      9 => [10],
      10 => [9, 1],
    }
  end

  test "bridges" do
    input = Day24.parse(
      ["0/2", "2/2", "2/3", "0/1"])
    assert Day24.bridges(input) == [
      [0],
      [1, 0, 0],
      [2, 0, 0],
      [3, 2, 2, 0, 0],
      [2, 2, 2, 0, 0],
      [3, 2, 2, 2, 2, 0, 0],
      [2, 2, 2, 0, 0],
      [3, 2, 2, 2, 2, 0, 0],
    ]

    input = Day24.parse(
      ["0/2", "2/2", "2/3", "3/4", "3/5", "0/1", "10/1", "9/10"])
    bridges = Day24.bridges(input)
    assert bridges |> length() == 16
    assert bridges |> Day24.strongest() == 31
    assert bridges |> Day24.strongest_longest() == 19
  end
end

map =
  with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 24), do: raw
  |> String.split("\n", trim: true)
  |> Day24.parse()

bridges = map |> Day24.bridges()
bridges |> Day24.strongest() |> IO.puts
bridges |> Day24.strongest_longest() |> IO.puts
