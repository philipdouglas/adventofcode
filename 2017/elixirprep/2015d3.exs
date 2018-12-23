defmodule Day do
    def deliver(instructions) do
        deliver(String.graphemes(instructions), MapSet.new([{0, 0}]), {0, 0})
    end

    def deliver([head | tail], seen, pos) do
        pos = follow_instruction(head, pos)
        deliver(tail, MapSet.put(seen, pos), pos)
    end

    def deliver([], seen, pos), do: MapSet.size(seen)

    def follow_instruction(instruction, pos) do
        case instruction do
            "^" -> {elem(pos, 0) + 1, elem(pos, 1)}
            ">" -> {elem(pos, 0), elem(pos, 1) + 1}
            "v" -> {elem(pos, 0) - 1, elem(pos, 1)}
            "<" -> {elem(pos, 0), elem(pos, 1) - 1}
        end
    end

    def robodeliver(instructions) do
        instructions
        |> String.graphemes
        |> deliver(MapSet.new([{0, 0}]), {0, 0}, {0, 0})
    end

    def deliver([head | tail], seen, first, second) do
        first = follow_instruction(head, first)
        deliver(tail, MapSet.put(seen, first), second, first)
    end

    def deliver([], seen, first, second), do: MapSet.size(seen)
end

IO.puts Day.deliver(">")
IO.puts Day.deliver("^>v<")
IO.puts Day.deliver("^v^v^v^v^v")

{:ok, input} = File.read "D:\\Dropbox\\adventofcode\\2015\\3.txt"

input |> String.trim |> Day.deliver |> IO.puts

IO.puts Day.robodeliver("^v")
IO.puts Day.robodeliver("^>v<")
IO.puts Day.robodeliver("^v^v^v^v^v")

input |> String.trim |> Day.robodeliver |> IO.puts
