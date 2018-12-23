defmodule Day21 do
  use Tensor

  defp parse_grid(input) do
    rows = String.split(input, "/")
    for row <- rows do
      for light <- String.graphemes(row) do
        case light do
          "#" -> 1
          "." -> 0
        end
      end
    end
    |> Matrix.new(length(rows), length(rows))
  end

  def parse(input) do
    input
    |> Enum.flat_map(fn(line) ->
      [from, to] = String.split(line, " => ")
      from = parse_grid(from)
      to = parse_grid(to)
      [
        &Matrix.flip_vertical/1,
        &Matrix.flip_horizontal/1,
        &Matrix.rotate_clockwise/1,
        &Matrix.rotate_counterclockwise/1,
      ]
      |> Enum.map(&(&1.(from)))
      |> Enum.flat_map(&([&1, Matrix.flip_horizontal(&1)]))
      |> Enum.map(&({Matrix.to_list(&1), to}))
    end)
    |> Map.new()
  end

  def break_up(state) do
    matrixsize = state |> Matrix.row(0) |> Vector.length()
    chunksize = if rem(matrixsize, 2) == 0, do: 2, else: 3
    offmax = div(matrixsize, chunksize) - 1
    for yoff <- 0..offmax, yoff = yoff * chunksize,
        xoff <- 0..offmax, xoff = xoff * chunksize do
      for y <- yoff..(yoff + chunksize) - 1 do
        for x <- xoff..(xoff + chunksize) - 1 do
          state[y][x]
        end
      end
      |> Matrix.new(chunksize, chunksize)
    end
  end

  def combine(matrices) do
    chunksize = matrices |> length() |> :math.sqrt() |> trunc()
    matrixsize =
      matrices
      |> Enum.at(0)
      |> Matrix.to_list()
      |> length()
      |> Kernel.*(chunksize)
    for matrices <- Enum.chunk_every(matrices, chunksize) do
      rows = for matrix <- matrices, do: Matrix.to_list(matrix)
      depth = rows |> Enum.at(0) |> length()
      for index <- 0..depth - 1, do: Enum.flat_map(rows, &(Enum.at(&1, index)))
    end
    |> Enum.concat()
    |> Matrix.new(matrixsize, matrixsize)
  end

  def apply(rules, iterations) do
    start = Matrix.new([[0, 1, 0], [0, 0, 1], [1, 1, 1]], 3, 3)
    1..iterations
    |> Enum.reduce(start, fn(_, state) ->
      state
      |> break_up()
      |> Enum.map(&(Map.get(rules, Matrix.to_list(&1))))
      |> combine()
    end)
  end

  def count(matrix) do
    matrix
    |> Matrix.to_sparse_map()
    |> Map.values()
    |> Enum.count()
  end
end

ExUnit.start()
defmodule Day21Test do
  use ExUnit.Case
  use Tensor

  test "parse" do
    input = [
      "../.# => ##./#../...",
      ".#./..#/### => #..#/..../..../#..#",
    ]
    three = Matrix.new([[1, 1, 0], [1, 0, 0], [0, 0, 0]], 3, 3)
    four = Matrix.new(
      [[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]], 4, 4)
    assert Day21.parse(input) == %{
      [[0, 0], [0, 1]] => three,
      [[0, 0], [1, 0]] => three,
      [[0, 1], [0, 0]] => three,
      [[1, 0], [0, 0]] => three,
      [[0, 1, 0],
       [0, 0, 1],
       [1, 1, 1]] => four,
      [[0, 1, 0],
       [1, 0, 0],
       [1, 1, 1]] => four,
      [[1, 1, 1],
       [0, 0, 1],
       [0, 1, 0]] => four,
      [[1, 1, 1],
       [1, 0, 0],
       [0, 1, 0]] => four,
      [[1, 0, 0],
       [1, 0, 1],
       [1, 1, 0]] => four,
      [[1, 1, 0],
       [1, 0, 1],
       [1, 0, 0]] => four,
      [[0, 0, 1],
       [1, 0, 1],
       [0, 1, 1]] => four,
      [[0, 1, 1],
       [1, 0, 1],
       [0, 0, 1]] => four,
    }
  end

  test "break_up" do
    input = Matrix.new([[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]], 4, 4)
    assert Day21.break_up(input) == [
        Matrix.new([[1, 0], [0, 0]], 2, 2),
        Matrix.new([[0, 1], [0, 0]], 2, 2),
        Matrix.new([[0, 0], [1, 0]], 2, 2),
        Matrix.new([[0, 0], [0, 1]], 2, 2),
      ]
    input = Matrix.new([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 3, 3)
    assert Day21.break_up(input) == [input]
  end

  test "combine" do
    input = [
      Matrix.new([[1, 0, 0], [0, 0, 0], [0, 0, 0]], 3, 3),
      Matrix.new([[1, 0, 1], [0, 0, 1], [0, 0, 1]], 3, 3),
      Matrix.new([[1, 0, 0], [0, 0, 0], [1, 0, 0]], 3, 3),
      Matrix.new([[1, 0, 1], [0, 0, 1], [1, 0, 1]], 3, 3),
    ]
    assert Day21.combine(input) == Matrix.new([
      [1, 0, 0, 1, 0, 1],
      [0, 0, 0, 0, 0, 1],
      [0, 0, 0, 0, 0, 1],
      [1, 0, 0, 1, 0, 1],
      [0, 0, 0, 0, 0, 1],
      [1, 0, 0, 1, 0, 1]], 6, 6)
    input = Matrix.new([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 3, 3)
    assert Day21.combine([input]) == input
  end

  test "apply" do
    input = [
      "../.# => ##./#../...",
      ".#./..#/### => #..#/..../..../#..#",
    ]
    rules = Day21.parse(input)
    result = Day21.apply(rules, 2)
    assert result == Matrix.new([
      [1, 1, 0, 1, 1, 0],
      [1, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0],
      [1, 1, 0, 1, 1, 0],
      [1, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0],
    ], 6, 6)
    assert Day21.count(result) == 12
  end

  test "reddit" do
    {:ok, raw} = File.read("day21_dootbootmoot.txt")
    result =
      raw
      |> String.split("\n", trim: true)
      |> Day21.parse()
      |> Day21.apply(5)
      |> Day21.count()
    assert result == 208
  end
end

rules =
  with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 21), do: raw
  |> String.split("\n", trim: true)
  |> Day21.parse()

import ExProf.Macro

profile do
rules |> Day21.apply(5) |> Day21.count() |> IO.puts()
end
# rules |> Day21.apply(18) |> Day21.count() |> IO.puts()
