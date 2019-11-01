# digits = split(strip(read("../.cache/input_2017_1", String)), "")
digits = ["1", "1", "2", "2"]
digits = parse.(Int, digits)
push!(digits, digits[1])
print(digits)
