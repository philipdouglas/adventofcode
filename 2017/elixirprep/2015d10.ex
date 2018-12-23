defmodule Day10 do
    def sequence(repeats) do
        1..repeats
        |> Enum.reduce(Integer.digits(1321131112), fn(_, prev) ->
            prev
            |> Enum.chunk_by(&(&1))
            |> Enum.flat_map(&([length(&1), Enum.at(&1, 0)]))
        end)
        |> length()
    end
end

IO.puts(Day10.sequence(40))
IO.puts(Day10.sequence(50))
