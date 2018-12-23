defmodule Day do
    def is_nice(string) do
        is_nice(String.graphemes(string), 0, false)
    end

    def is_nice([char | string], vowels, pair) do
        vowels = cond do
            String.match?(char, ~r/[aeiou]/) -> vowels + 1
            true -> vowels
        end
        next = Enum.at(string, 0)
        cond do
            char == next -> is_nice(string, vowels, true)
            next != nil and char <> next in ["ab", "cd", "pq", "xy"] -> false
            true -> is_nice(string, vowels, pair)
        end
    end

    def is_nice([], vowels, true) when vowels >= 3, do: true
    def is_nice([], _, _), do: false

    def is_nice2(string) do
        is_nice2(String.graphemes(string), false, false)
    end

    def is_nice2([char | [next | string]], doublepair, splitpair) do
        next2 = Enum.at(string, 0)
        doublepair = cond do
            doublepair -> doublepair
            String.match?(Enum.join(string), ~r/.*#{char}#{next}.*/) -> true
            true -> false
        end
        cond do
            char == next2 -> is_nice2([next | string], doublepair, true)
            true -> is_nice2([next | string], doublepair, splitpair)
        end
    end

    def is_nice2(_, true, true), do: true
    def is_nice2(string, _, _) when length(string) <= 1, do: false
end

IO.puts(Day.is_nice("ugknbfddgicrmopn"))
IO.puts(Day.is_nice("aaa"))
IO.puts(Day.is_nice("jchzalrnumimnmhp"))
IO.puts(Day.is_nice("haegwjzuvuyypxyu"))
IO.puts(Day.is_nice("dvszwmarrgswjxmb"))

input = File.stream!("D:\\Dropbox\\adventofcode\\2015\\5.txt" )
|> Stream.map(&String.trim_trailing/1)
|> Enum.to_list

input
|> Enum.count(&Day.is_nice/1)
|> IO.puts

IO.puts(Day.is_nice2("qjhvhtzxzqqjkmpb"))
IO.puts(Day.is_nice2("xxyxx"))
IO.puts(Day.is_nice2("uurcxstgmygtbstg"))
IO.puts(Day.is_nice2("ieodomkazucvgmuy"))


input
|> Enum.count(&Day.is_nice2/1)
|> IO.puts
