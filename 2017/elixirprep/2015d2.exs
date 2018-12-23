defmodule Day2 do
    def paper_area(dims) do
        [l, w, h] = for d <- String.split(dims, "x"), do: String.to_integer(d)
        2*l*w + 2*w*h + 2*h*l + Enum.min([l * w, w * h, l * h])
    end

    def ribbon_length(dims) do
        [l, w, h] = for d <- String.split(dims, "x"), do: String.to_integer(d)
        Enum.min([2*l + 2*w, 2*l + 2*h, 2*w + 2*h]) + l*w*h
    end
end

IO.puts Day2.paper_area("2x3x4")
IO.puts Day2.paper_area("1x1x10")

input = File.stream!("D:\\Dropbox\\adventofcode\\2015\\2.txt" )
|> Stream.map(&String.trim_trailing/1)
|> Enum.to_list
input
|> Enum.reduce(0, &(Day2.paper_area(&1) + &2))
|> IO.puts

IO.puts Day2.ribbon_length("2x3x4")
IO.puts Day2.ribbon_length("1x1x10")

input
|> Enum.reduce(0, &(Day2.ribbon_length(&1) + &2))
|> IO.puts
