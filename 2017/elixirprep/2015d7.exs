use Bitwise

defmodule Day do
    def parse(instruction) do
        matches =
        ~r{(?:(\d+|[a-z]+) )?(?:(NOT|AND|OR|LSHIFT|RSHIFT) )?(\d+|[a-z]+) -> (\d+|[a-z]+)}
        |> Regex.run(instruction, capture: :all_but_first)
        case matches do
            ["", "", value, id] -> %{id => value}
            ["", "NOT", op1, id] -> %{id => {:not, op1}}
            [op1, "AND", op2, id] -> %{id => {:and, op1, op2}}
            [op1, "OR", op2, id] -> %{id => {:or, op1, op2}}
            [op1, "LSHIFT", op2, id] -> %{id => {:lshift, op1, op2}}
            [op1, "RSHIFT", op2, id] -> %{id => {:rshift, op1, op2}}
        end
    end

    def construct_circuit([]), do: %{}

    def construct_circuit([instruction | instructions]) do
        Map.merge(parse(instruction), construct_circuit(instructions))
    end

    def get(circuit, id) do
        # IO.inspect(id)
        # IO.puts("get #{id}")
        cond do
            Map.has_key?(circuit, id) -> get(circuit, Map.get(circuit, id))
            is_integer(id) -> id
            id -> String.to_integer(id)
        end
    end

    def evaluate(circuit, id, {op, op1}) do
        # IO.puts("#{id}: #{op} #{op1}")
        circuit = evaluate(circuit, op1)
        Map.put(circuit, id, execute(op, get(circuit, op1)))
    end

    def evaluate(circuit, id, {op, op1, op2}) do
        # IO.puts("#{id}: #{op} #{op1} #{op2}")
        circuit = circuit |> evaluate(op1) |> evaluate(op2)
        Map.put(circuit, id, execute(op, get(circuit, op1), get(circuit, op2)))
    end

    def evaluate(circuit, id, value) do
        # IO.puts("#{id}: #{value}")
        if Map.has_key?(circuit, value) do
            circuit = evaluate(circuit, value, Map.get(circuit, value))
            Map.put(circuit, id, Map.get(circuit, value))
        else
            circuit = evaluate(circuit, value)
        end
    end

    def evaluate(circuit, id) do
        # IO.puts("#{id}?")
        if Map.has_key?(circuit, id) do
            evaluate(circuit, id, Map.get(circuit, id))
        else
            circuit
        end
    end

    def execute(:not, op1) do
        bnot(op1)
    end
    def execute(:and, op1, op2) do
        band(op1, op2)
    end
    def execute(:or, op1, op2) do
        bor(op1, op2)
    end
    def execute(:lshift, op1, op2) do
        op1 <<< op2
    end
    def execute(:rshift, op1, op2) do
        op1 >>> op2
    end
end

# "123 -> x" |> Day.parse |> IO.inspect
# "456 -> y" |> Day.parse |> IO.inspect
# "x AND y -> d" |> Day.parse |> IO.inspect
# "x OR y -> e" |> Day.parse |> IO.inspect
# "x LSHIFT 2 -> f" |> Day.parse |> IO.inspect
# "y RSHIFT 2 -> g" |> Day.parse |> IO.inspect
# "NOT x -> h" |> Day.parse |> IO.inspect
# "NOT y -> i" |> Day.parse |> IO.inspect

input = AdventOfCodeHelper.get_input(2015, 7)
|> case do
    {:ok, content} -> content
end
|> String.split("\n", trim: true)

input
|> Day.construct_circuit
|> Day.evaluate("a")
|> Map.get("a")
|> IO.inspect

input
|> Kernel.++(["16076 -> b"])
|> Day.construct_circuit
|> Day.evaluate("a")
|> Map.get("a")
|> IO.inspect
