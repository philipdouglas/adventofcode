defmodule Day6 do
    def find_loop(memory), do: find_loop([], memory)

    def find_loop(seen, current) do
        case current in seen do
            true -> {length(seen), Enum.find_index(seen, &(&1 === current)) + 1}
            false -> find_loop([current | seen], gen_next(current))
        end
    end

    def gen_next(state) do
        state = Enum.with_index(state)
        width = length(state)
        {distval, distindex} = Enum.max_by(state, fn({num, index}) -> num end)
        allinc = div(distval, width)
        overflow = rem(distval, width)
        Enum.map(state, fn({value, index}) ->
            value = if index == distindex, do: 0, else: value
            offset = index - distindex
            offset = offset + (if offset <= 0, do: width, else: 0)
            value + allinc + (if offset <= overflow, do: 1, else: 0)
        end)
    end
end


ExUnit.start

defmodule Day6Test do
    use ExUnit.Case

    test "gen_next" do
        next = Day6.gen_next([0, 2, 7, 0])
        assert next == [2, 4, 1, 2]
        next = Day6.gen_next(next)
        assert next == [3, 1, 2, 3]
        next = Day6.gen_next(next)
        assert next == [0, 2, 3, 4]
        next = Day6.gen_next(next)
        assert next == [1, 3, 4, 1]
        next = Day6.gen_next(next)
        assert next == [2, 4, 1, 2]
    end

    test "find_loop" do
        assert Day6.find_loop([0, 2, 7, 0]) == {5, 4}
    end
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017,6), do: raw
    |> String.trim("\n")
    |> String.split("\t", trim: true)
    |> Enum.map(&String.to_integer/1)

input
|> Day6.find_loop()
|> IO.inspect()
