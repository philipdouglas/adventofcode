defmodule Day25 do
  def run(rules, state, diag, pos \\ 0, cycle \\ 0, tape \\ %{})
  def run(_, _, diag, _, cycle, tape) when cycle > diag do
    tape |> Map.values() |> Enum.sum()
  end
  def run(rules, state, diag, pos, cycle, tape) do
    {new_val, direction, new_state} =
      Map.get(rules, state) |> Map.get(Map.get(tape, pos, 0))
    new_pos = pos + if(direction == :right, do: 1, else: -1)
    run(rules, new_state, diag, new_pos, cycle + 1, Map.put(tape, pos, new_val))
  end
end

ExUnit.start()
defmodule Day25Test do
  use ExUnit.Case

  test "run" do
    rules = %{
      :a => %{
        0 => {1, :right, :b},
        1 => {0, :left, :b},
      },
      :b => %{
        0 => {1, :left, :a},
        1 => {0, :right, :a},
      }
    }
    assert Day25.run(rules, :a, 6) == 3
  end
end

rules = %{
  :a => %{0 => {1, :right, :b}, 1 => {0, :left, :b}},
  :b => %{0 => {0, :right, :c}, 1 => {1, :left, :b}},
  :c => %{0 => {1, :right, :d}, 1 => {0, :left, :a}},
  :d => %{0 => {1, :left, :e}, 1 => {1, :left, :f}},
  :e => %{0 => {1, :left, :a}, 1 => {0, :left, :d}},
  :f => %{0 => {1, :right, :a}, 1 => {1, :left, :e}},
}

rules |> Day25.run(:a, 12629077) |> IO.puts()
