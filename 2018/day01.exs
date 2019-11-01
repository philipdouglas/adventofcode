defmodule Day1 do
  def part2(changes) do
    changes
    |> Stream.cycle
    |> Stream.scan(fn(change, freq) -> freq + change end)
    |> Enum.reduce_while(MapSet.new([0]), fn (freq, seen) ->
      if MapSet.member?(seen, freq) do
        {:halt, freq}
      else
        {:cont, MapSet.put(seen, freq)}
      end
    end)
  end
end

ExUnit.start

defmodule Day1Test do
  use ExUnit.Case

  test "part2" do
    assert Day1.part2([1, -2, 3, 1]) == 2
    assert Day1.part2([+1, -1]) == 0
    assert Day1.part2([+3, +3, +4, -2, -4]) == 10
    assert Day1.part2([-6, +3, +8, +5, -6]) == 5
    assert Day1.part2([+7, +7, -2, -7, -4]) == 14
  end
end

input = with {:ok, raw} = File.read(".cache/input_2018_01.txt"), do: raw
|> String.trim()
|> String.split("\n")
|> Enum.map(&String.to_integer/1)

input |> Enum.sum |> IO.puts

input
|> Day1.part2
|> IO.puts()
