defmodule Day16 do
    def make_dancers(number) do
        alphabet = for n <- ?a..?z, do: << n :: utf8 >>
        Enum.take(alphabet, number)
    end

    def parse(instruction) do
        ~r{([sxp])([a-z0-9]+)/?([a-z0-9]+)?}
        |> Regex.run(instruction, capture: :all_but_first)
        |> Enum.map(&(if &1 =~ ~r/[0-9]+/, do: String.to_integer(&1), else: &1))
    end

    def execute(["s", num], dancers) do
        Enum.slice(dancers, -num..-1) ++ Enum.slice(dancers, 0..-(num + 1))
    end
    def execute(["x", a, b], dancers) do
        # dancers
        # |> List.replace_at(a, Enum.at(dancers, b))
        # |> List.replace_at(b, Enum.at(dancers, a))

    end
    def execute(["p", a, b], dancers) do
        a = Enum.find_index(dancers, &(&1 == a))
        b = Enum.find_index(dancers, &(&1 == b))
        execute(["x", a, b], dancers)
    end

    def dance(instructions, dancers) do
        instructions
        |> Enum.map(&parse/1)
        |> Enum.reduce(make_dancers(dancers), &execute/2)
        |> Enum.join()
    end

    def part2(instructions, dancers) do
        instructions = instructions |> Enum.map(&parse/1)
        [last | seen] =
            Stream.iterate(make_dancers(dancers), fn(dancers) ->
                Enum.reduce(instructions, dancers, &execute/2)
            end)
            |> Stream.scan([], &([&1 | &2]))
            |> Stream.drop_while(fn([last | seen]) -> last not in seen end)
            |> Enum.at(0)
        looplen = Enum.find_index(seen, &(&1 == last)) + 1
        leftover = rem(1000000000 - length(seen) + looplen, looplen)
        seen |> Enum.at(looplen - 1 - leftover)
    end
end

ExUnit.start()
defmodule Day16Test do
    use ExUnit.Case

    test "parse" do
        assert Day16.parse("s1") == ["s", 1]
        assert Day16.parse("x3/4") == ["x", 3, 4]
        assert Day16.parse("pe/b") == ["p", "e", "b"]
    end

    test "make_dancers" do
        assert Day16.make_dancers(5) == ["a", "b", "c", "d", "e"]
    end

    test "execute s" do
        assert Day16.execute(["s", 3], ["a", "b", "c", "d", "e"]) ==
            ["c", "d", "e", "a", "b"]
    end

    test "dance" do
        instructions = [
            "s1",
            "x3/4",
            "pe/b",
        ]
        assert Day16.dance(instructions, 5) == "baedc"
    end
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 16), do: raw
    |> String.split(",", trim: true)

# import ExProf.Macro

# profile do
input |> Day16.dance(16) |> IO.puts()
input |> Day16.part2(16) |> IO.puts()
# end
