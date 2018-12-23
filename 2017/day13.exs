defmodule Day13 do
    def parse(lines) do
        lines
        |> Enum.map(&(String.split(&1, ": ")))
        |> Enum.map(fn(pair) -> Enum.map(pair, &String.to_integer/1) end)
        |> Enum.map(fn(pair) -> List.to_tuple(pair) end)
        # Longer ranges are more likely to catch so sorting makes part 2
        # slightly quicker
        |> Enum.sort_by(fn({_, range}) -> range end)
    end

    def part1(firewall) do
        Enum.reduce(firewall, 0, fn({depth, range}, total) ->
            total + severity(depth, range) end)
    end

    def severity(depth, range) do
        if rem(depth, (range - 1) * 2) == 0, do: depth * range, else: 0
    end

    def part2(firewall) do
        Stream.iterate(0, &(&1 + 1))
        |> Stream.reject(&(Day13.clean_route?(&1, firewall)))
        |> Enum.at(0)
    end

    def clean_route?(offset, firewall) do
        Enum.any?(firewall, fn({depth, range}) ->
            rem(depth + offset, (range - 1) * 2) == 0 end)
    end
end

ExUnit.start()
defmodule Day13Test do
    use ExUnit.Case

    test "test" do
        firewall = Day13.parse(["0: 3", "1: 2", "4: 4", "6: 4"])
        assert firewall == [{1, 2}, {0, 3}, {4, 4}, {6, 4}]
        assert Day13.part1(firewall) == 24
        assert Day13.part2(firewall) == 10
    end
end

firewall =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 13), do: raw
    |> String.split("\n", trim: true)
    |> Day13.parse()

firewall |> Day13.part1() |> IO.puts()
firewall |> Day13.part2() |> IO.puts()
