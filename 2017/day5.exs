defmodule Day5 do
    def execute({pc, prog}) do
        jump = Map.get(prog, pc)
        {pc + jump, Map.put(prog, pc, jump + 1)}
    end

    def run(prog, function) do
        prog = 0..length(prog) |> Enum.zip(prog) |> Map.new()
        run(prog, 0, 0, function)
    end
    def run(prog, pc, steps, _) when pc < 0 or pc >= map_size(prog) do
        steps
    end
    def run(prog, pc, steps, function) do
        {pc, prog} = function.({pc, prog})
        run(prog, pc, steps + 1, function)
    end

    def execute2({pc, prog}) do
        jump = Map.get(prog, pc)
        replace = cond do
            jump >= 3 -> jump - 1
            true -> jump + 1
        end
        {pc + jump, Map.put(prog, pc, replace)}
    end
end


ExUnit.start

defmodule Day5Test do
    use ExUnit.Case

    # test "execute" do
    #     state = Day5.execute({0, [0, 3, 0, 1, -3]})
    #     assert state == {0, [1, 3, 0, 1, -3]}
    #     state = Day5.execute(state)
    #     assert state == {1, [2, 3, 0, 1, -3]}
    #     state = Day5.execute(state)
    #     assert state == {4, [2, 4, 0, 1, -3]}
    #     state = Day5.execute(state)
    #     assert state == {1, [2, 4, 0, 1, -2]}
    #     state = Day5.execute(state)
    #     assert state == {5, [2, 5, 0, 1, -2]}
    # end

    test "run" do
        assert Day5.run([0, 3, 0, 1, -3], &Day5.execute/1) == 5
    end

    test "run 2" do
        assert Day5.run([0, 3, 0, 1, -3], &Day5.execute2/1) == 10
    end
end


input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017,5), do: raw
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_integer/1)

input
|> Day5.run(&Day5.execute/1)
|> IO.puts()

input
|> Day5.run(&Day5.execute2/1)
|> IO.puts()
