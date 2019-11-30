defmodule AOC.Mixfile do
  use Mix.Project

  def project do
    [
      app: :aoc,
      version: "0.1.0",
      deps: deps(),
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      # {:dep_from_hexpm, "~> 0.3.0"},
      # {:dep_from_git, git: "https://github.com/elixir-lang/my_dep.git", tag: "0.1.0"},
      # {:advent_of_code_helper, github: "FreakyDug/Advent-Of-Code", branch: "master"},
      {:advent_of_code_helper, path: "../Advent-Of-Code"},
      {:exprof, "~> 0.2.0"},
      {:tensor, "~> 2.0"},
      {:xxhash, "~> 0.2.1"},
    ]
  end
end
