defmodule Day18 do
    def parse(input) do
        input
        |> Enum.map(fn(instruction) ->
            ~r/([a-z]{3}) ([a-z0-9]+) ?([\-a-z0-9]+)?/
            |> Regex.run(instruction, capture: :all_but_first)
            |> Enum.map(&(
                if &1 =~ ~r/^[\-0-9]+$/, do: String.to_integer(&1), else: &1))
        end)
        |> Enum.map(fn([cmd | args]) -> [String.to_atom(cmd) | args] end)
        |> Enum.map(&List.to_tuple/1)
    end

    def getval(regs, op) do
        if is_integer(op), do: op, else: Map.get(regs, op, 0)
    end

    def execute({:snd, x}, pc, regs) do
        {pc + 1, Map.put(regs, "_snd", getval(regs, x))}
    end
    def execute({:rcv, x}, pc, regs) do
        {pc + 1, case getval(regs, x) do
            0 -> regs
            _ -> Map.put(regs, "_rcv", Map.get(regs, "_snd"))
        end}
    end
    def execute({:set, x, y}, pc, regs) do
        {pc + 1, Map.put(regs, x, getval(regs, y))}
    end
    def execute({:add, x, y}, pc, regs) do
        {pc + 1, Map.put(regs, x, getval(regs, x) + getval(regs, y))}
    end
    def execute({:mul, x, y}, pc, regs) do
        {pc + 1, Map.put(regs, x, getval(regs, x) * getval(regs, y))}
    end
    def execute({:mod, x, y}, pc, regs) do
        {pc + 1, Map.put(regs, x, rem(getval(regs, x), getval(regs, y)))}
    end
    def execute({:jgz, x, y}, pc, regs) do
        {pc + if(getval(regs, x) > 0, do: getval(regs, y), else: 1), regs}
    end

    def part1(program, pc \\ 0, regs \\ %{}) do
        if Map.has_key?(regs, "_rcv") do
            Map.get(regs, "_rcv")
        else
            {pc, regs} = execute(Enum.at(program, pc), pc, regs)
            part1(program, pc, regs)
        end
    end

    def execute2({:snd, x}, pc, regs) do
        send(Map.get(regs, "_other"), getval(regs, x))
        {pc + 1, Map.put(regs, "_sent", Map.get(regs, "_sent", 0) + 1)}
    end
    def execute2({:rcv, x}, pc, regs) do
        receive do
            val -> {pc + 1, Map.put(regs, x, val)}
        after
            10 -> {:deadlock, regs}
        end
    end
    def execute2(instruction, pc, regs), do: execute(instruction, pc, regs)

    def run2(program, regs, pc \\ 0) do
        case execute2(Enum.at(program, pc), pc, regs) do
            {:deadlock, regs} -> regs
            {pc, regs} -> run2(program, regs, pc)
        end
    end

    def part2(program) do
        pid = spawn(Day18, :run2, [program, %{"_other" => self(), "p" => 0}])
        run2(program, %{"_other" => pid, "p" => 1})
        |> Map.get("_sent")
    end
end

ExUnit.start()
defmodule Day18Test do
    use ExUnit.Case

    test "part1" do
        program = [
            "set a 1",
            "add a 2",
            "mul a a",
            "mod a 5",
            "snd a",
            "set a 0",
            "rcv a",
            "jgz a -1",
            "set a 1",
            "jgz a -2",
        ]
        program = Day18.parse(program)
        assert program == [
            {:set, "a", 1},
            {:add, "a", 2},
            {:mul, "a", "a"},
            {:mod, "a", 5},
            {:snd, "a"},
            {:set, "a", 0},
            {:rcv, "a"},
            {:jgz, "a", -1},
            {:set, "a", 1},
            {:jgz, "a", -2},
        ]
        assert Day18.part1(program) == 4
    end

    test "part2" do
        program = [
            {:snd, 1},
            {:snd, 2},
            {:snd, "p"},
            {:rcv, "a"},
            {:rcv, "b"},
            {:rcv, "c"},
            {:rcv, "d"},
        ]
        assert Day18.part2(program) == 3
    end
end

program =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 18), do: raw
    |> String.split("\n", trim: true)
    |> Day18.parse()

program |> Day18.part1() |> IO.puts()
program |> Day18.part2() |> IO.puts()
