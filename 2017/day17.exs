defmodule Day17 do
    def step(new, sequence, steps) do
        sequence
        |> Stream.cycle()
        |> Stream.drop(rem(steps, length(sequence)))
        |> Enum.take(length(sequence))
        |> List.insert_at(-1, new)
    end

    def part1(steps) do
        1..2017
        |> Enum.reduce([0], fn(new, sequence) ->
            step(new, sequence, steps)
        end)
        |> Enum.at(0)
    end

    def part2(steps, max, num \\ 1, prev_pos \\ 0, best \\ 0)
    def part2(_, max, num, _, best) when num > max, do: best
    def part2(steps, max, num, prev_pos, best) do
        new_pos = rem(prev_pos + steps, num) + 1
        best = if new_pos == 1, do: num, else: best
        part2(steps, max, num + 1, new_pos, best)
    end
end

ExUnit.start()
defmodule Day17Test do
    use ExUnit.Case

    test "1", do: assert Day17.step(1, [0], 3) == [0, 1]
    test "2", do: assert Day17.step(2, [0, 1], 3) == [1, 0, 2]
    test "3", do: assert Day17.step(3, [1, 0, 2], 3) == [1, 0, 2, 3]
    test "4", do: assert Day17.step(4, [1, 0, 2, 3], 3) == [3, 1, 0, 2, 4]
    test "5", do: assert Day17.step(5, [3, 1, 0, 2, 4], 3) == [2, 4, 3, 1, 0, 5]
    test "6", do: assert Day17.step(6, [2, 4, 3, 1, 0, 5], 3) == [1, 0, 5, 2, 4, 3, 6]

    test "3 steps", do: assert Day17.part1(3) == 638

    test "part2", do: assert Day17.part2(3, 10) == 9
end

input = 394

input |> Day17.part1() |> IO.puts()
# import ExProf.Macro
# profile do
input |> Day17.part2(50000000) |> IO.inspect()
# end
