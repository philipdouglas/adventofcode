defmodule Day2 do
    def difference(numbers) do
        Enum.max(numbers) - Enum.min(numbers)
    end

    def pairs([head | tail]) do
        for(other <- tail, do: {head, other}) |> Enum.concat(pairs(tail))
    end
    def pairs([]), do: []

    def even_divide(numbers) do
        pairs = numbers |> Enum.sort() |> Enum.reverse() |> pairs()
        for {big, smol} <- pairs, rem(big, smol) == 0 do div(big, smol) end
        |> Enum.at(0)
    end

end

ExUnit.start

defmodule Day1Test do
    use ExUnit.Case

    test "difference" do
        assert Day2.difference([5, 1, 9, 5]) == 8
        assert Day2.difference([7, 5, 3]) == 4
        assert Day2.difference([2, 4, 6, 8]) == 6
    end

    test "even_divide" do
        assert Day2.even_divide([3, 8, 6, 5]) == 2
        assert Day2.even_divide([9, 4, 7, 3]) == 3
        assert Day2.even_divide([5, 9, 2, 8]) == 4
    end

    test "pairs" do
        assert Day2.pairs([1, 2, 3]) == [{1, 2}, {1, 3}, {2, 3}]
    end
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 2), do: raw
    |> String.split("\n", trim: true)
    |> Enum.map(fn (row) ->
        row
        |> String.split("\t", trim: true)
        |> Enum.map(&String.to_integer/1)
    end)

input
|> Enum.map(&Day2.difference/1)
|> Enum.sum()
|> IO.puts()

input
|> Enum.map(&Day2.even_divide/1)
|> Enum.sum()
|> IO.puts()
