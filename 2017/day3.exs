defmodule Day3 do
    def part1(target) do
        {x, y} = coords() |> Enum.at(target-1)
        :erlang.abs(x) + :erlang.abs(y)
    end

    def coord_add({x, y}, {m, n}) do
        {x + m, y + n}
    end

    def coords() do
        stream = Stream.iterate(0, &(&1 + 1))
        |> Stream.flat_map(&([&1, &1]))
        |> Stream.zip(Stream.cycle([{1, 0}, {0, 1}, {-1, 0}, {0, -1}]))
        |> Stream.flat_map(fn({n, coord}) -> for _ <- 0..n, do: coord end)
        |> Stream.scan({0, 0}, &coord_add/2)
        Stream.concat([{0, 0}], stream)
    end

    def part2(target) do
        {result, map} =
            coords()
            |> Stream.scan({0, %{}}, &path/2)
            |> Stream.reject(fn ({number, _}) -> number < target end)
            |> Enum.at(0)
        result
    end

    def path(next, {_, map}) do
        value = compute_next(next, map)
        {value, Map.put(map, next, value)}
    end

    def compute_next({0, 0}, _), do: 1
    def compute_next(coord, map) do
        for dx <- -1..1, dy <- -1..1 do
            Map.get(map, coord_add(coord, {dx, dy}), 0)
        end
        |> Enum.sum()
    end
end


ExUnit.start

defmodule Day3Test do
    use ExUnit.Case

    test "part1" do
        assert Day3.part1(1) == 0
        assert Day3.part1(2) == 1
        assert Day3.part1(3) == 2
        assert Day3.part1(4) == 1
        assert Day3.part1(5) == 2
        assert Day3.part1(6) == 1
        assert Day3.part1(7) == 2
        assert Day3.part1(8) == 1
        assert Day3.part1(9) == 2
        assert Day3.part1(10) == 3
        assert Day3.part1(11) == 2
        assert Day3.part1(12) == 3
        assert Day3.part1(13) == 4
        assert Day3.part1(14) == 3
        assert Day3.part1(15) == 2
        assert Day3.part1(16) == 3
        assert Day3.part1(17) == 4
        assert Day3.part1(18) == 3
        assert Day3.part1(19) == 2
        assert Day3.part1(20) == 3
        assert Day3.part1(21) == 4
        assert Day3.part1(22) == 3
        assert Day3.part1(23) == 2
        assert Day3.part1(1024) == 31
    end

    test "coords" do
        assert Day3.coords() |> Enum.take(7) == [
            {0, 0}, {1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}, {-1, -1}]
    end

    test "compute_next" do
        assert Day3.compute_next({1, 1}, %{{0, 0} => 1, {1, 0} => 1}) == 2
        assert Day3.compute_next(
            {0, 1}, %{{0, 0} => 1, {1, 0} => 1, {1, 1} => 2}) == 4
    end

    test "part2" do
        assert Day3.part2(30) == 54
        assert Day3.part2(360) == 362
    end
end

input = 265149

input |> Day3.part1() |> IO.puts
input |> Day3.part2() |> IO.puts
