use Bitwise

defmodule KnotHash do
    def rotate(enumerable, amount) do
        {front, back} = Enum.split(enumerable, amount)
        back ++ front
    end

    def tie(len, {string, pos, skip}) do
        {section, remainder} = string |> rotate(pos) |> Enum.split(len)
        string = Enum.reverse(section) ++ remainder |> rotate(-pos)
        pos = rem(pos + len + skip, length(string))
        {string, pos, skip + 1}
    end

    def singleround(input, size \\ 256) do
        {[one, two | _], _, _} =
            Enum.reduce(input, {Enum.to_list(0..size - 1), 0, 0}, &tie/2)
        one * two
    end

    def hex(input, size \\ 256) do
        input = Enum.to_list(input) ++ [17, 31, 73, 47, 23]
        1..64
        |> Enum.reduce({Enum.to_list(0..size - 1), 0, 0}, fn(_, state) ->
            Enum.reduce(input, state, &tie/2) end)
        |> elem(0)
        |> Enum.chunk_every(16)
        |> Enum.map(fn(chunk) -> Enum.reduce(chunk, 0, &bxor/2) end)
        |> Enum.map(&(Integer.to_string(&1, 16) |> String.pad_leading(2, "0")))
        |> Enum.join()
    end

    def binary(input, size \\ 256) do
        KnotHash.hex(input, size)
        |> String.graphemes()
        |> Enum.map(&(&1
            |> Integer.parse(16)
            |> elem(0)
            |> Integer.to_string(2)
            |> String.pad_leading(4, "0")))
        |> Enum.flat_map(&String.graphemes/1)
    end
end
