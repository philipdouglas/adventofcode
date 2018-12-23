defmodule Day1 do
    def what_floor(instructions, floor, count) when length(instructions) == 0 do
        floor
    end

    def what_floor(instructions, floor, count) when floor == -1 do
        count
    end

    def what_floor(instructions, floor, count) do
        [head | tail] = instructions
        floor =
            case head do
                "(" -> floor + 1
                ")" -> floor - 1
            end
        what_floor(tail, floor, count + 1)
    end
end

{:ok, input} = File.read "D:\\Dropbox\\adventofcode\\2015\\1input.txt"
input |> String.graphemes |> Day1.what_floor(0, 0) |> IO.puts
