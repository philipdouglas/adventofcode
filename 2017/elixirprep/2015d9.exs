defmodule Day9 do
    def parse(string) do
        ~r{([^ ]+) to ([^ ]+) = (\d+)}
        |> Regex.run(string, capture: :all_but_first)
    end

    def build_map([head | tail]) do
        [from, to, distance] = parse(head)
        distance = String.to_integer(distance)
        build_map(tail)
        |> Map.put_new(from, %{})
        |> Map.put_new(to, %{})
        |> put_in([from, to], distance)
        |> put_in([to, from], distance)
    end
    def build_map([]), do: %{}

    def follow_route([from | [to | rest]], map) do
        get_in(map, [from, to]) + follow_route([to | rest], map)
    end
    def follow_route([_ | []], _), do: 0

    # From http://rosettacode.org/wiki/Permutations#Elixir
    def permute([]), do: [[]]
    def permute(list) do
        for x <- list, y <- permute(list -- [x]), do: [x|y]
    end
end

ExUnit.start

defmodule Day9Test do
    use ExUnit.Case

    test "parse" do
        assert Day9.parse("London to Dublin = 464") == ["London", "Dublin", "464"]
    end

    test "follow_route" do
        map = Day9.build_map([
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141",
        ])
        assert Day9.follow_route(["London", "Dublin", "Belfast"], map) == 605
    end
end

input = with {:ok, raw} <- AdventOfCodeHelper.get_input(2015, 9), do: raw
|> String.split("\n", trim: true)

map = input
|> Day9.build_map

route_lengths = Map.keys(map)
|> Day9.permute
|> Enum.map(&(Day9.follow_route(&1, map)))

route_lengths
|> Enum.min
|> IO.puts

route_lengths
|> Enum.max
|> IO.puts

