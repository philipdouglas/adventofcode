defmodule Day do
    def parse_pair(pair) do
        String.split(pair, ",")
        |> Enum.map(&String.to_integer/1)
    end

    def parse(instruction) do
        [instruction | args] =
        ~r{(turn on|turn off|toggle) (\d+,\d+) through (\d+,\d+)}
        |> Regex.run(instruction, capture: :all_but_first)
        instruction = case instruction do
            "turn on" -> :on
            "turn off" -> :off
            "toggle" -> :toggle
        end
        [instruction | Enum.map(args, &parse_pair/1)]
    end

    def coords(size) do
        for x <- 0..size - 1,
            y <- 0..size - 1,
            do: {x, y}
    end

    def count_lights(instructions, size) do
        coords(size)
        |> Enum.reduce(0, &check_light(instructions, &1, &2))
    end

    def check_light(instructions, coord, total) do
        case apply_instructions(instructions, coord) do
            true -> 1
            false -> 0
        end + total
    end

    def apply_instructions([[instruction, from, to] | instructions], {x, y}) do
        if in_bounds?(from, to, x, y) do
            case instruction do
                :on -> true
                :off -> false
                :toggle -> not apply_instructions(instructions, {x, y})
            end
        else
            apply_instructions(instructions, {x, y})
        end
    end

    def apply_instructions([], _) do
        false
    end

    def in_bounds?([fromx , fromy], [tox , toy], x, y) do
        fromx <= x and fromy <= y and tox >= x and toy >= y
    end

    def count_lights2(instructions, size) do
        coords(size)
        |> Enum.reduce(0, &check_light2(instructions, &1, &2))
    end

    def check_light2(instructions, coord, total) do
        apply_instructions2(instructions, coord) + total
    end

    def apply_instructions2([[instruction, from, to] | instructions], {x, y}) do
        if in_bounds?(from, to, x, y) do
            case instruction do
                :on -> 1
                :off -> -1
                :toggle -> 2
            end
        else
            0
        end
        |> Kernel.+(apply_instructions2(instructions, {x, y}))
        |> max(0)
    end

    def apply_instructions2([], _) do
        0
    end
end

# IO.puts(Day.in_bounds?([0, 0], [999, 999], 3, 4))
# IO.inspect(Day.parse("turn off 102,229 through 674,529"))

["turn on 0,0 through 999,0"]
|> Enum.map(&Day.parse/1)
|> Enum.reverse
|> Day.count_lights(1000)
|> IO.puts

input = AdventOfCodeHelper.get_input(2015, 6)
|> case do
    {:ok, content} -> content
end
|> String.split("\n", trim: true)
|> Enum.map(&Day.parse/1)

input
|> Enum.reverse
|> Day.count_lights(1000)
|> IO.puts

input
|> Enum.reverse
|> Day.count_lights2(1000)
|> IO.puts


