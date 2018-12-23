defmodule Day9 do
    def score(string) do
        score(String.graphemes(string), 0, false)
    end

    def score(["{" | tail], depth, false), do: score(tail, depth + 1, false)
    def score(["}" | tail], depth, false) do
        {score, count} = score(tail, depth - 1, false)
        {depth + score, count}
    end
    def score(["!", _ | tail], depth, garbg), do: score(tail, depth, garbg)
    def score(["<" | tail], depth, false), do: score(tail, depth, true)
    def score([">" | tail], depth, true), do: score(tail, depth, false)
    def score([_ | tail], depth, true) do
        {score, count} = score(tail, depth, true)
        {score, count + 1}
    end
    def score([_ | tail], depth, false), do: score(tail, depth, false)
    def score([], _, _), do: {0, 0}
end

ExUnit.start()

defmodule Day9Test do
    use ExUnit.Case

    test "1", do: assert Day9.score("{}") == {1, 0}
    test "2", do: assert Day9.score("{{{}}}") == {6, 0}
    test "3", do: assert Day9.score("{{},{}}") == {5, 0}
    test "4", do: assert Day9.score("{{{},{},{{}}}}") == {16, 0}
    test "5", do: assert Day9.score("{<a>,<a>,<a>,<a>}") == {1, 4}
    test "6", do: assert Day9.score("{{<ab>},{<ab>},{<ab>},{<ab>}}") == {9, 8}
    test "7", do: assert Day9.score("{{<!!>},{<!!>},{<!!>},{<!!>}}") == {9, 0}
    test "8", do: assert Day9.score("{{<a!>},{<a!>},{<a!>},{<ab>}}") == {3, 17}
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 9), do: raw
    |> String.trim("\n")

input |> Day9.score() |> IO.inspect()
