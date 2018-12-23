defmodule Day7 do
    def get_weight({weight, _}), do: weight

    def walk(data, nodename) do
        {weight, children} = Map.get(data, nodename)
        childweights = Enum.map(children, &(walk(data, &1)))
        answer = if !Enum.empty?(childweights) do
            childweights
            |> Enum.map(fn({_, answer}) -> answer end)
            |> Enum.max()
        else 0 end
        childweights = Enum.map(childweights, &get_weight/1)
        answer = cond do
            answer != 0 -> answer
            Enum.uniq(childweights) |> length() > 1 ->
                [{{wrong, name}, 1}, {{right, _}, _}] = childweights
                    |> Enum.zip(children)
                    |> Enum.sort_by(&get_weight/1)
                    |> Enum.chunk_by(&get_weight/1)
                    |> Enum.sort_by(&length/1)
                    |> Enum.map(&({hd(&1), length(&1)}))
                {value, _} = Map.get(data, name)
                value + (right - wrong)
            true -> 0
        end
        {weight + Enum.sum(childweights), answer}
    end
end

input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017,7), do: raw
    |> String.split("\n", trim: true)

nodes = input
    |> Enum.map(fn(line) ->
        [name, weight] = ~r/([a-z]+) \((\d+)\)/
            |> Regex.run(line, capture: :all_but_first)
        children = ~r/[a-z]+(?=, |$)/
            |> Regex.scan(line)
            |> List.flatten()
        {name, {String.to_integer(weight), children}}
    end)
    |> Enum.into(%{})

children = nodes
    |> Map.values()
    |> Enum.flat_map(fn({_, children}) -> children end)
    |> MapSet.new()

part1 = nodes
    |> Map.keys()
    |> MapSet.new()
    |> MapSet.difference(children)
    |> Enum.at(0)
part1 |> IO.puts()

nodes
|> Day7.walk(part1)
|> elem(1)
|> IO.puts()

# Original part 1 hack
# [[part1]] = input
#     |> Enum.flat_map(&(Regex.split(~r/[^a-z]+/, &1)))
#     |> Enum.sort()
#     |> Enum.chunk_by(&(&1))
#     |> Enum.reject(&(length(&1) > 1))
# part1 |> IO.puts
