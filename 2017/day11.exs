defmodule Day11 do
    def solution(route) do
        steps = route |> Enum.scan([0, 0, 0], &step/2) |> Enum.map(&dist/1)
        {Enum.at(steps, -1), Enum.max(steps)}
    end

    def dist(coord), do: coord |> Enum.map(&abs/1) |> Enum.max()
    def add([x, y, z], [dx, dy, dz]), do: [x + dx, y + dy, z + dz]

    def step("n",  pos), do: add(pos, [ 0,  1, -1])
    def step("nw", pos), do: add(pos, [ 1,  0, -1])
    def step("sw", pos), do: add(pos, [ 1, -1,  0])
    def step("s",  pos), do: add(pos, [ 0, -1,  1])
    def step("se", pos), do: add(pos, [-1,  0,  1])
    def step("ne", pos), do: add(pos, [-1,  1,  0])
end

ExUnit.start()

defmodule Day11Test do
    use ExUnit.Case

    test "1", do: assert Day11.solution(["ne","ne","ne"]) == {3, 3}
    test "2", do: assert Day11.solution(["ne","ne","sw","sw"]) == {0, 2}
    test "3", do: assert Day11.solution(["ne","ne","s","s"]) == {2, 2}
    test "4", do: assert Day11.solution(["se","sw","se","sw","sw"]) == {3, 3}
end

with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 11), do: raw
|> String.trim("\n")
|> String.split(",", trim: true)
|> Day11.solution()
|> IO.inspect()

