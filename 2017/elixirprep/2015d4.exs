defmodule Day do
    def check_hash(input, zeroes) do
        bits = zeroes * 4
        case :crypto.hash(:md5, input) do
            <<0 :: size(bits), _ :: bitstring>> -> true
            _ -> false
        end
    end

    def mine(key, zeroes \\ 5, number \\ 0) do
        case check_hash([key | to_string(number)], zeroes) do
            true -> number
            false -> mine(key, zeroes, number + 1)
        end
    end
end

IO.puts Day.mine("abcdef")
IO.puts Day.mine("pqrstuv")
IO.puts Day.mine("iwrupvqb")
IO.puts Day.mine("iwrupvqb", 6)
d
