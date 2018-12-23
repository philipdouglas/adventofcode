defmodule Day8 do
    def parse(line) do
        ~r/([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([<>=!]+) (-?\d+)/
        |> Regex.run(line, capture: :all_but_first)
    end

    def execute([opreg, op, opval, condreg, comparator, ref], registers) do
        condreg = Map.get(registers, condreg, 0)

        if condition(condreg, comparator, String.to_integer(ref)) do
            opregval = Map.get(registers, opreg, 0)
            opval = String.to_integer(opval)
            Map.put(registers, opreg, operate(opregval, op, opval))
        else registers end
    end

    def condition(regval, operator, ref) do
        apply(Kernel, String.to_atom(operator), [regval, ref])
    end

    def operate(regval, "inc", operand), do: regval + operand
    def operate(regval, "dec", operand), do: regval - operand
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 8), do: raw
    |> String.split("\n", trim: true)

max_values =
    input
    |> Enum.map(&Day8.parse/1)
    |> Enum.scan(%{}, &Day8.execute/2)
    |> Enum.map(&(&1 |> Map.values() |> Enum.max()))

max_values |> List.last() |> IO.puts()
max_values |> Enum.max() |> IO.puts()
