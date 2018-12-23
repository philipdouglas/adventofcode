defmodule Day23 do
  def parse(input) do
    input
    |> String.split("\n", trim: true)
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

  def execute({:set, x, y}, pc, regs) do
    {pc + 1, Map.put(regs, x, getval(regs, y))}
  end
  def execute({:sub, x, y}, pc, regs) do
    {pc + 1, Map.put(regs, x, getval(regs, x) - getval(regs, y))}
  end
  def execute({:mul, x, y}, pc, regs) do
    regs = Map.put(regs, "_mul_count", Map.get(regs, "_mul_count", 0) + 1)
    {pc + 1, Map.put(regs, x, getval(regs, x) * getval(regs, y))}
  end
  def execute({:jnz, x, y}, pc, regs) do
    {pc + if(getval(regs, x) != 0, do: getval(regs, y), else: 1), regs}
  end

  def part1(program, pc \\ 0, regs \\ %{})
  def part1(program, pc, regs) when pc >= length(program) do
    Map.get(regs, "_mul_count")
  end
  def part1(program, pc, regs) do
    {pc, regs} = execute(Enum.at(program, pc), pc, regs)
    part1(program, pc, regs)
  end

  # Stolen from http://wende.github.io/2015/09/07/Elixir-n-prime-numbers.html
  def is_prime?(x) do
    2..x |> Enum.filter(&(rem(x, &1) == 0)) |> length() |> Kernel.==(1)
  end

  def part2() do
    105700
    |> Stream.iterate(&(&1 + 17))
    |> Stream.take(1001)
    |> Stream.reject(&is_prime?/1)
    |> Enum.count()
  end
end

program =
  with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 23), do: raw
  |> Day23.parse()

program |> Day23.part1() |> IO.puts()
Day23.part2() |> IO.puts()
