with open('1input.txt') as input_file:
    inp = input_file.read()

print(inp.count('(') - inp.count(')'))
floor = 0
count = 0
for char in inp:
    count += 1
    if char == '(':
        floor += 1
    if char == ')':
        floor -= 1
    if floor < 0:
        break
print(count)
