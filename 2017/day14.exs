defmodule Day14 do
    require KnotHash

    def memory(input) do
        0..127
        |> Enum.map(&('#{input}-#{&1}' |> KnotHash.binary()))
    end

    def memmap(input) do
        0..127
        |> Enum.flat_map(fn(row) ->
            '#{input}-#{row}'
            |> KnotHash.binary()
            |> Enum.with_index()
            |> Enum.map(fn({value, col}) -> {{row, col}, value} end)
        end)
        |> Map.new()
    end

    def part1(memory) do
        memory
        |> Map.values()
        |> Enum.reject(&(&1 == "0"))
        |> Enum.count()
    end

    def getcell({row, col}, memory)
            when row < 0 or col < 0
            when row >= length(memory) or col >= length(memory) do
        nil
    end
    def getcell({row, col}, memory) do
        Map.get(memory, {row, col})
    end

    def coord_add({x, y}, {m, n}) do
        {x + m, y + n}
    end
    def distance({x, y}, {m, n}) do
        abs(x - m) + abs(y - n)
    end

    def findregion(pos, memory, seen) do
        [{-1, 0}, {0, -1}, {1, 0}, {0, 1}]
        |> Enum.map(&(coord_add(pos, &1)))
        |> Enum.reduce(MapSet.put(seen, pos), fn(neighbour, seen) ->
            cond do
                neighbour in seen -> seen
                getcell(neighbour, memory) == "1" ->
                    findregion(neighbour, memory, seen)
                true -> seen
            end
        end)
    end

    def search(coords, memory, seen \\ MapSet.new(), total \\ 0)
    def search([pos | tail], memory, seen, total) do
        {region, seen} = cond do
            pos in seen -> {0, seen}
            getcell(pos, memory) == "1" -> {1, findregion(pos, memory, seen)}
            true -> {0, MapSet.put(seen, pos)}
        end
        search(tail, memory, seen, total + region)
    end
    def search([], _, _, total), do: total

    def part2(memory) do
        0..127
        |> Enum.flat_map(fn(row) -> 0..127 |> Enum.map(&({row, &1})) end)
        |> search(memory)
    end
end


ExUnit.start()

defmodule Day14Test do
    use ExUnit.Case

    test "flqrgnkx" do
        testmem = "flqrgnkx" |> Day14.memmap()
        assert testmem |> Day14.part1() == 8108
        assert testmem |> Day14.part2() == 1242
    end

    # test "findregion" do
    #     memory = [
    #         String.graphemes("11010100"),
    #         String.graphemes("01010101"),
    #         String.graphemes("00001010"),
    #         String.graphemes("10101101"),
    #         String.graphemes("01101000"),
    #         String.graphemes("11001001"),
    #         String.graphemes("01000100"),
    #         String.graphemes("11010110"),
    #     ]
    #     assert Day14.findregion({0, 0}, memory, MapSet.new()) == MapSet.new([
    #         {0, 0}, {0, 1}, {1, 1}])
    # end
end

memory = "ffayrhll" |> Day14.memmap()

# import ExProf.Macro

# profile do
memory |> Day14.part1() |> IO.puts()
memory |> Day14.part2() |> IO.puts()
# end
