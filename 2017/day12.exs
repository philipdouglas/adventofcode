defmodule Day12 do
    def makemap(lines) do
        lines
        |> Enum.map(&(String.split(&1, " <-> ")))
        |> Enum.map(fn([left, right]) -> {left, String.split(right, ", ")} end)
        |> Map.new()
    end

    def findgroup(map, id) do
        {childs, map} = Map.pop(map, id, [])
        childs
        |> Enum.map(&(findgroup(map, &1)))
        |> Enum.reduce(MapSet.new([id]), &MapSet.union/2)
    end

    def findgroups(map, groups \\ [])
    def findgroups(map, groups) when map == %{}, do: groups
    def findgroups(map, groups) do
        group = findgroup(map, map |> Map.keys() |> hd())
        map |> Map.drop(group) |> findgroups([group | groups])
    end
end

map =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 12), do: raw
    |> String.split("\n", trim: true)
    |> Day12.makemap()

map
|> Day12.findgroup("0")
|> MapSet.size()
|> IO.puts()

map
|> Day12.findgroups()
|> length()
|> IO.puts()
