defmodule Day1 do
    def captcha(numbers) do
        check(numbers ++ Enum.take(numbers, 1))
    end

    def check([first | [second | rest]]) do
        check([second | rest]) + if first == second, do: first, else: 0
    end

    def check([_ | []]), do: 0

    def captcha2(numbers) do
        [first, second] = Enum.chunk_every(numbers, div(length(numbers), 2))
        check2(numbers, second ++ first)
    end

    def check2([numhead | numtail], [halfhead | halftail]) do
        check2(numtail, halftail) + if numhead == halfhead, do: numhead, else: 0
    end

    def check2([], []), do: 0

    def unified(numbers, offset \\ 1) do
        offnum = Stream.cycle(numbers)
        |> Stream.drop(offset)
        for({num, off} <- Enum.zip(numbers, offnum), num == off, do: num)
        |> Enum.sum()
    end
end

input = with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 1), do: raw
|> String.trim()
|> String.graphemes()
|> Enum.map(&String.to_integer/1)

ExUnit.start

defmodule Day1Test do
    use ExUnit.Case

    test "captcha" do
        assert Day1.captcha([1, 1, 2, 2]) == 3
        assert Day1.captcha([1, 1, 1, 1]) == 4
        assert Day1.captcha([1, 2, 3, 4]) == 0
        assert Day1.captcha([9, 1, 2, 1, 2, 1, 2, 9]) == 9
    end

    test "captcha2" do
        assert Day1.captcha2([1, 2, 1, 2]) == 6
        assert Day1.captcha2([1, 2, 2, 1]) == 0
        assert Day1.captcha2([1, 2, 3, 4, 2, 5]) == 4
        assert Day1.captcha2([1, 2, 3, 1, 2, 3]) == 12
        assert Day1.captcha2([1, 2, 1, 3, 1, 4, 1, 5]) == 4
    end

    test "unified" do
        assert Day1.unified([1, 1, 2, 2]) == 3
        assert Day1.unified([1, 1, 1, 1]) == 4
        assert Day1.unified([1, 2, 3, 4]) == 0
        assert Day1.unified([9, 1, 2, 1, 2, 1, 2, 9]) == 9
    end

    test "unified2" do
        assert Day1.unified([1, 2, 1, 2], 2) == 6
        assert Day1.unified([1, 2, 2, 1], 2) == 0
        assert Day1.unified([1, 2, 3, 4, 2, 5], 3) == 4
        assert Day1.unified([1, 2, 3, 1, 2, 3], 3) == 12
        assert Day1.unified([1, 2, 1, 3, 1, 4, 1, 5], 4) == 4
    end
end

input |> Day1.captcha() |> IO.puts()
input |> Day1.captcha2() |> IO.puts()

input |> Day1.unified() |> IO.puts()
input |> Day1.unified(div(length(input), 2)) |> IO.puts
