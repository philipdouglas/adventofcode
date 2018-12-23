defmodule Day15 do
    use Bitwise, only: :operators

    def generate(prev, factor), do: prev * factor |> rem(2147483647)
    def agenerate(prev), do: generate(prev, 16807)
    def bgenerate(prev), do: generate(prev, 48271)
    def generator(start, func) do
        Stream.iterate(start, func) |> Stream.drop(1)
    end

    def pairstream(aval, bval) do
        agen = generator(aval, &agenerate/1)
        bgen = generator(bval, &bgenerate/1)
        Stream.zip(agen, bgen)
    end

    def pickypairstream(aval, bval) do
        agen = generator(aval, &agenerate/1) |> Stream.filter(&(rem(&1, 4) == 0))
        bgen = generator(bval, &bgenerate/1) |> Stream.filter(&(rem(&1, 8) == 0))
        Stream.zip(agen, bgen)
    end

    def filter({aval, bval}) do
        (aval &&& 0xFFFF) == (bval &&& 0xFFFF)
    end

    def count(pairstream, limit) do
        pairstream
        |> Stream.take(limit)
        |> Stream.filter(&filter/1)
        |> Enum.count()
    end
end


ExUnit.start()

defmodule Day15Test do
    use ExUnit.Case

    test "pairstream" do
        firstfive =
            Day15.pairstream(65, 8921)
            |> Enum.take(5)
        assert firstfive == [
            {   1092455,  430625591},
            {1181022009, 1233683848},
            { 245556042, 1431495498},
            {1744312007,  137874439},
            {1352636452,  285222916},
        ]
    end

    test "pickypairstream" do
        firstfive =
            Day15.pickypairstream(65, 8921)
            |> Enum.take(5)
        assert firstfive == [
            {1352636452, 1233683848},
            {1992081072,  862516352},
            { 530830436, 1159784568},
            {1980017072, 1616057672},
            { 740335192,  412269392},
        ]
    end

    # test "part1" do
    #     assert Day15.pairstream(65, 8921) |> Day15.count(40000000) == 588
    # end

    # test "part2" do
    #     assert Day15.pickypairstream(65, 8921) |> Day15.count(5000000) == 309
    # end
end

import ExProf.Macro

profile do
    Day15.pairstream(591, 393) |> Day15.count(40000000) |> IO.puts()
    # Day15.pickypairstream(591, 393) |> Day15.count(5000000) |> IO.puts()
end
