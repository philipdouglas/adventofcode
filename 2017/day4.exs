input =
    with {:ok, raw} <- AdventOfCodeHelper.get_input(2017,4), do: raw
    |> String.split("\n", trim: true)
    |> Enum.map(&(String.split(&1, " ")))

input
|> Enum.filter(&(Enum.uniq(&1) == &1))
|> Enum.count()
|> IO.puts()

input
|> Enum.map(fn(pass) -> Enum.map(pass, &String.graphemes/1) end)
|> Enum.map(fn(pass) -> Enum.map(pass, &Enum.sort/1) end)
|> Enum.filter(&(Enum.uniq(&1) == &1))
|> Enum.count()
|> IO.puts()
