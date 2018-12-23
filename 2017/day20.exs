defmodule Day20 do
  def parse(input) do
    for particle <- input do
      ~r/p=< *([^>]+)>, v=< *([^>]+)>, a=< *([^>]+)>/
      |> Regex.run(particle, capture: :all_but_first)
      |> Enum.zip([:p, :v, :a])
      |> Enum.map(fn({coord, letter}) ->
        coord =
          coord
          |> String.split(",")
          |> Enum.map(&String.to_integer/1)
          |> List.to_tuple()
        {letter, coord}
      end)
    end
  end

  def coord_add({x, y, z}, {dx, dy, dz}) do
    {x + dx, y + dy, z + dz}
  end

  def advance([p: p, v: v, a: a]) do
    v = coord_add(v, a)
    p = coord_add(p, v)
    [p: p, v: v, a: a]
  end

  def dist_at_t([{:p, {x, y, z}}, {:v, {vx, vy, vz}}, {:a, {ax, ay, az}}], t) do
    for {p, v, a} <- [{x, vx, ax}, {y, vy, ay}, {z, vz, az}] do
      (p + (v * t) - ((a * t * t) / 2))
    end
    |> Enum.map(&abs/1)
    |> Enum.sum()
  end

  def closest(particles, t \\ 10000) do
    particles
    |> Enum.map(&(dist_at_t(&1, t)))
    |> Enum.with_index()
    |> Enum.min_by(fn({genpos, _}) -> genpos end)
    |> elem(1)
  end

  def collisions(particles, t \\ 0)
  def collisions(particles, t) when t > 100, do: Enum.count(particles)
  def collisions(particles, t) do
    particles
    |> Enum.map(&advance/1)
    |> Enum.sort_by(&(Keyword.get(&1, :p)))
    |> Enum.chunk_by(&(Keyword.get(&1, :p)))
    |> Enum.reject(&(length(&1) > 1))
    |> Enum.flat_map(&(&1))
    |> collisions(t + 1)
  end
end

ExUnit.start()
defmodule Day20Test do
  use ExUnit.Case

  test "parse" do
    input = [
      "p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
      "p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>",
    ]
    assert Day20.parse(input) == [
      [p: {3,0,0}, v: {2,0,0}, a: {-1,0,0}],
      [p: {4,0,0}, v: {0,0,0}, a: {-2,0,0}],
    ]
  end

  test "closest" do
    particles = [
      [p: {3,0,0}, v: {2,0,0}, a: {-1,0,0}],
      [p: {4,0,0}, v: {0,0,0}, a: {-2,0,0}],
    ]
    assert Day20.closest(particles) == 0
  end
end

particles =
  with {:ok, raw} <- AdventOfCodeHelper.get_input(2017, 20), do: raw
  |> String.split("\n", trim: true)
  |> Day20.parse()

particles |> Day20.closest() |> IO.puts()
particles |> Day20.collisions() |> IO.puts()
