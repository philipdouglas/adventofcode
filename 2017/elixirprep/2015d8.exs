defmodule Day8 do
    def replace_chars(_, escaped, zeroes) do
        cond do
            String.length(zeroes) != 0 -> ""
            true -> "1"
        end
    end

    def count_chars(string) do
        mem = ~r/(?:(\\(?:[^x]|x[0-9a-fA-F]{2}))|(?!\\)("))/
        |> Regex.replace(string, &replace_chars/3)
        {String.length(string), String.length(mem)}
    end

    def encode(string) do
        encoded = ~r/[\\"]/
        |> Regex.replace(string, &("\\#{&1}"))
        ~s("#{encoded}")
    end

    def part1(string) do
        {code, mem} = count_chars(string)
        code - mem n
    end

    def part2(string) do
        {code, _} = count_chars(string)
        encoded = encode(string)
        String.length(encoded) - code
    end
end

input = AdventOfCodeHelper.get_input(2015, 8)
|> case do
    {:ok, content} -> content
end
|> String.split("\n", trim: true)

ExUnit.start

defmodule Day8Test do
    use ExUnit.Case, async: true

    test "count_chars" do
        assert Day8.count_chars(~s("")) == {2, 0}
        assert Day8.count_chars(~s("abc")) == {5, 3}
        assert Day8.count_chars(~s("aaa\\"aaa")) == {10, 7}
        assert Day8.count_chars(~s("\\x27")) == {6, 1}
    end

    test "encode" do
        assert Day8.encode(~s("")) == ~s("\\"\\"")
        assert Day8.encode(~s("abc")) == ~s("\\"abc\\"")
        assert Day8.encode(~s("aaa\\"aaa")) == ~s("\\"aaa\\\\\\"aaa\\"")
        assert Day8.encode(~s("\\x27")) == ~s("\\"\\\\x27\\"")
    end
end

input
|> Enum.map(&Day8.part1/1)
|> Enum.sum()
|> IO.puts


input
|> Enum.map(&Day8.part2/1)
|> Enum.sum()
|> IO.puts
